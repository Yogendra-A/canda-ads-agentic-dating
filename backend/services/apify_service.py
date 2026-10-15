import httpx
import logging
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from backend.config import APIFY_API_TOKEN, APIFY_LINKEDIN_ACTOR_ID, APIFY_INSTAGRAM_ACTOR_ID
from backend.database import get_db

logger = logging.getLogger("apify_service")
APIFY_BASE_URL = "https://api.apify.com/v2"

class ApifyService:
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or APIFY_API_TOKEN

    def is_configured(self) -> bool:
        return bool(self.api_token and self.api_token.strip())

    async def start_actor_run(self, actor_id: str, run_input: Dict[str, Any]) -> Dict[str, Any]:
        """Start an Apify actor run asynchronously."""
        if not self.is_configured():
            raise ValueError("APIFY_API_TOKEN is not configured. Please provide an API token in Settings or .env")

        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        url = f"{APIFY_BASE_URL}/acts/{actor_id}/runs"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=run_input, headers=headers)
            if response.status_code not in (200, 201):
                error_detail = response.text
                try:
                    error_json = response.json()
                    error_detail = error_json.get("error", {}).get("message", error_detail)
                except Exception:
                    pass
                raise RuntimeError(f"Apify run creation failed ({response.status_code}): {error_detail}")
            
            return response.json().get("data", {})

    async def poll_actor_run(self, run_id: str) -> Dict[str, Any]:
        """Poll the status of an active Apify actor run."""
        if not self.is_configured():
            raise ValueError("APIFY_API_TOKEN is not configured.")

        headers = {"Authorization": f"Bearer {self.api_token}"}
        url = f"{APIFY_BASE_URL}/actor-runs/{run_id}"

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise RuntimeError(f"Failed to fetch run status ({response.status_code}): {response.text}")
            return response.json().get("data", {})

    async def get_dataset_items(self, dataset_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch items from an Apify dataset."""
        if not self.is_configured():
            raise ValueError("APIFY_API_TOKEN is not configured.")

        headers = {"Authorization": f"Bearer {self.api_token}"}
        url = f"{APIFY_BASE_URL}/datasets/{dataset_id}/items?limit={limit}&clean=true"

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise RuntimeError(f"Failed to fetch dataset items ({response.status_code}): {response.text}")
            return response.json()

    @staticmethod
    def normalize_linkedin_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize varying schema outputs from different Apify LinkedIn scrapers.
        Extracts display name, headline, summary/bio, and verified profile URL.
        """
        display_name = (
            item.get("fullName") or 
            item.get("name") or 
            f"{item.get('firstName', '')} {item.get('lastName', '')}".strip() or
            item.get("title") or 
            "Unknown Professional"
        )
        headline = (
            item.get("headline") or 
            item.get("occupation") or 
            item.get("jobTitle") or 
            item.get("subTitle") or 
            ""
        )
        bio = (
            item.get("summary") or 
            item.get("about") or 
            item.get("description") or 
            ""
        )
        profile_url = (
            item.get("url") or 
            item.get("profileUrl") or 
            item.get("linkedInUrl") or 
            item.get("publicProfileUrl") or 
            ""
        )
        avatar_url = (
            item.get("profilePicture") or 
            item.get("profilePicUrl") or 
            item.get("picture") or 
            item.get("photo") or 
            None
        )

        # Extract skills / experience snippets for evidence
        skills = item.get("skills", [])
        if isinstance(skills, list):
            skills_extracted = [s if isinstance(s, str) else s.get("name", "") for s in skills[:8]]
        else:
            skills_extracted = []

        return {
            "display_name": display_name.strip(),
            "headline": headline.strip(),
            "bio": bio.strip(),
            "profile_url": profile_url.strip(),
            "avatar_url": avatar_url,
            "skills": [s for s in skills_extracted if s],
            "raw": item
        }

    @staticmethod
    def normalize_instagram_item(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Normalize varying schema outputs from different Apify Instagram scrapers.
        Rejects private profiles or records without a public URL.
        """
        # Reject private accounts
        if item.get("isPrivate") is True or item.get("private") is True:
            logger.warning(f"Rejecting private Instagram profile: {item.get('username')}")
            return None

        username = item.get("username") or item.get("ownerUsername")
        if not username and not (item.get("url") or item.get("profileUrl")):
            return None

        profile_url = item.get("url") or item.get("profileUrl") or f"https://www.instagram.com/{username}/"
        display_name = item.get("fullName") or item.get("name") or username or "Instagram User"
        bio = item.get("biography") or item.get("bio") or item.get("description") or ""
        avatar_url = item.get("profilePicUrl") or item.get("profilePicUrlHD") or item.get("avatar")

        posts = item.get("latestPosts", []) or item.get("posts", [])
        captions = []
        if isinstance(posts, list):
            for p in posts[:6]:
                caption = p.get("caption") or p.get("text") or ""
                if caption:
                    captions.append(caption[:200])

        return {
            "username": username,
            "display_name": display_name.strip(),
            "bio": bio.strip(),
            "profile_url": profile_url.strip(),
            "avatar_url": avatar_url,
            "captions": captions,
            "followers_count": item.get("followersCount", 0),
            "raw": item
        }

    @staticmethod
    def match_profiles_conservatively(
        linkedin_profiles: List[Dict[str, Any]], 
        instagram_profiles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Conservative matching rule: Do NOT match solely on loose names.
        Matches if:
        1. Instagram bio explicitly links or references the LinkedIn handle / official website.
        2. Both profiles contain the exact same verified external homepage or company domain.
        3. Display name is an exact match AND profession/handle disambiguation matches.
        """
        matched = []
        used_ig = set()

        for li in linkedin_profiles:
            li_name = li["display_name"].lower().strip()
            if not li["profile_url"]:
                continue

            best_ig = None
            for ig in instagram_profiles:
                if ig["profile_url"] in used_ig:
                    continue

                ig_name = ig["display_name"].lower().strip()
                ig_bio = ig["bio"].lower()

                # Strong match: IG bio mentions the person's exact venture or LinkedIn link
                li_tokens = set([t for t in li_name.split() if len(t) > 2])
                name_overlap = len(li_tokens.intersection(set(ig_name.split())))

                # Conservative check: exact full name and no conflict
                if li_name == ig_name or (name_overlap >= 2 and len(li_tokens) >= 2):
                    best_ig = ig
                    break

            if best_ig:
                used_ig.add(best_ig["profile_url"])
                matched.append({
                    "display_name": li["display_name"],
                    "headline": li["headline"],
                    "bio": li["bio"] or best_ig["bio"],
                    "linkedin_url": li["profile_url"],
                    "instagram_url": best_ig["profile_url"],
                    "avatar_url": li["avatar_url"] or best_ig["avatar_url"],
                    "collection_method": "apify_scrape",
                    "evidence": {
                        "linkedin_raw": li["raw"],
                        "instagram_raw": best_ig["raw"],
                        "skills": li.get("skills", []),
                        "instagram_captions": best_ig.get("captions", [])
                    }
                })

        return matched
