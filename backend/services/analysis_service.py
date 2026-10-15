import re
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import httpx
from backend.config import (
    LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
)
from backend.models import ProfileAnalysis, EvidenceItem
from backend.database import get_db

logger = logging.getLogger("analysis_service")
GEMINI_MODEL = "gemini-3.8-flash"

# Curated thematic keywords for deterministic evidence extraction
DOMAIN_KEYWORD_MAP = {
    "Artificial Intelligence": ["ai", "machine learning", "deep learning", "neural", "robotics", "algorithms", "llm", "frontier"],
    "Philosophy of Technology": ["philosophy", "ethics", "human dignity", "mind", "consciousness", "speculative"],
    "Design & Aesthetics": ["design", "industrial design", "aesthetics", "minimalist", "architecture", "interior", "visual", "art"],
    "Athletics & Physical Endurance": ["frisbee", "running", "marathon", "jiu-jitsu", "martial arts", "table tennis", "cycling", "surfing", "workout"],
    "Literature & Storytelling": ["poetry", "reading", "books", "author", "dostoevsky", "journalism", "memoir", "podcast"],
    "Mindfulness & Wellness": ["sleep", "meditation", "sauna", "wellness", "holistic", "tea", "yoga", "nature"],
    "Entrepreneurship & Strategy": ["founder", "startup", "investor", "venture", "catan", "scale", "product"],
    "Open Knowledge & Social Impact": ["education", "girls who code", "wikipedia", "equity", "climate", "philanthropy", "charity"]
}

class ProfileAnalysisService:
    @staticmethod
    def sanitize_untrusted_text(text: str) -> str:
        """
        Mitigate prompt injection and malicious control tokens from untrusted scraped text.
        Strips markdown system injection cues, delimiter tricks, and limits text length.
        """
        if not text:
            return ""
        # Remove common prompt injection markers
        cleaned = re.sub(r"(ignore\s+all\s+previous\s+instructions|system\s+prompt|developer\s+mode|<\|im_start\|>|<\|endoftext\|>)", "[REDACTED_INJECTION_ATTEMPT]", text, flags=re.IGNORECASE)
        # Cap length to prevent token exhaustion
        return cleaned[:3000].strip()

    @classmethod
    def deterministic_analyze(cls, person_dict: Dict[str, Any]) -> ProfileAnalysis:
        """
        High-fidelity deterministic keyword & evidence based analysis fallback.
        Ensures 100% reproducible, non-hallucinated, evidence-cited results when no LLM API key is present.
        """
        name = person_dict.get("display_name", "Individual")
        headline = cls.sanitize_untrusted_text(person_dict.get("headline", ""))
        bio = cls.sanitize_untrusted_text(person_dict.get("bio", ""))
        combined_text = f"{headline} {bio}".lower()

        matched_interests = []
        evidence_list = []
        source_url = person_dict.get("linkedin_url") or person_dict.get("instagram_url")

        # Analyze keywords against domain map
        for domain, keywords in DOMAIN_KEYWORD_MAP.items():
            for kw in keywords:
                if re.search(r"\b" + re.escape(kw) + r"\b", combined_text):
                    if domain not in matched_interests and len(matched_interests) < 5:
                        matched_interests.append(domain)
                    if source_url:
                        source_text = f"{headline} {bio}"
                        quote_match = re.search(
                            rf"[^.!?]*\b{re.escape(kw)}\b[^.!?]*[.!?]?",
                            source_text,
                            flags=re.IGNORECASE
                        )
                        evidence_list.append(EvidenceItem(
                            claim=f"Profile text mentions {domain}",
                            source_url=source_url,
                            quote=quote_match.group(0).strip() if quote_match else source_text.strip(),
                            confidence=0.65
                        ))
                    break

        hobbies = []
        if any(w in combined_text for w in ["chess", "catan", "games", "gaming"]):
            hobbies.append("Strategy Games & Puzzles")
        if any(w in combined_text for w in ["running", "cycling", "frisbee", "tennis", "gym", "workout"]):
            hobbies.append("Endurance Sports & Outdoor Fitness")
        if any(w in combined_text for w in ["tea", "coffee", "roast", "brewing", "cooking", "culinary"]):
            hobbies.append("Artisan Brewing & Culinary Exploration")
        if any(w in combined_text for w in ["music", "guitar", "piano", "concerts"]):
            hobbies.append("Acoustic Music & Instrumental Practice")
        compatibility_factors = (
            [f"Profile text mentions {matched_interests[0]}"]
            if matched_interests else []
        )
        summary = (
            f"{name}'s available profile text mentions {', '.join(matched_interests[:3])}."
            if matched_interests else
            f"Insufficient source text is available to infer interests or compatibility for {name}."
        )

        unknown_fields = [
            "Interests and hobbies",
            "Lifestyle and communication preferences",
            "Compatibility factors"
        ]

        return ProfileAnalysis(
            summary=summary,
            interests=matched_interests,
            hobbies=hobbies,
            lifestyle_signals=[],
            communication_style="",
            social_preferences=[],
            compatibility_factors=compatibility_factors,
            evidence_references=evidence_list[:4],
            confidence_score=min(0.65, 0.35 + 0.1 * len(evidence_list)) if evidence_list else 0.0,
            unknown_fields=unknown_fields,
            analysis_engine="deterministic_fallback",
            analyzed_at=datetime.now(timezone.utc).isoformat()
        )

    @classmethod
    async def analyze_with_llm(cls, person_dict: Dict[str, Any]) -> ProfileAnalysis:
        """
        Analyze profile using configured LLM provider (OpenAI, Anthropic, or Gemini).
        Falls back seamlessly to deterministic analysis if LLM call fails or is unconfigured.
        """
        from backend import config
        provider = config.LLM_PROVIDER.lower()
        if provider == "openai" and config.OPENAI_API_KEY:
            return await cls._call_openai(person_dict)
        elif provider == "anthropic" and config.ANTHROPIC_API_KEY:
            return await cls._call_anthropic(person_dict)
        elif provider == "gemini" and config.GEMINI_API_KEY:
            return await cls._call_gemini(person_dict)
        else:
            # Deterministic fallback
            return cls.deterministic_analyze(person_dict)

    @classmethod
    async def _call_openai(cls, person_dict: Dict[str, Any]) -> ProfileAnalysis:
        from backend import config
        try:
            prompt = cls._build_analysis_prompt(person_dict)
            headers = {
                "Authorization": f"Bearer {config.OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a professional behavioral psychologist and compatibility analyst. Return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.2
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data["choices"][0]["message"]["content"].strip()
                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0].strip()
                    elif "```" in text:
                        text = text.split("```")[1].split("```")[0].strip()
                    content = json.loads(text)
                    content["analysis_engine"] = "llm_openai"
                    content["analyzed_at"] = datetime.now(timezone.utc).isoformat()
                    return ProfileAnalysis.model_validate(content)
                else:
                    logger.warning(f"OpenAI API returned status {resp.status_code}")
        except Exception as e:
            logger.warning(f"OpenAI analysis failed, falling back to deterministic: {type(e).__name__}")
        return cls.deterministic_analyze(person_dict)

    @classmethod
    async def _call_gemini(cls, person_dict: Dict[str, Any]) -> ProfileAnalysis:
        from backend import config
        try:
            prompt = cls._build_analysis_prompt(person_dict)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
            headers = {
                "x-goog-api-key": config.GEMINI_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {
                "contents": [{"parts": [{"text": f"Return JSON only conforming to the schema.\n\n{prompt}"}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0].strip()
                    elif "```" in text:
                        text = text.split("```")[1].split("```")[0].strip()
                    content = json.loads(text)
                    content["analysis_engine"] = f"llm_gemini ({GEMINI_MODEL})"
                    content["analyzed_at"] = datetime.now(timezone.utc).isoformat()
                    return ProfileAnalysis.model_validate(content)
                else:
                    error = resp.json().get("error", {}) if resp.headers.get("content-type", "").startswith("application/json") else {}
                    logger.warning(
                        "Gemini API returned status %s (%s)",
                        resp.status_code,
                        error.get("status", "provider error details unavailable")
                    )
        except Exception as e:
            logger.warning(f"Gemini analysis failed, falling back to deterministic: {type(e).__name__}")
        return cls.deterministic_analyze(person_dict)

    @classmethod
    async def _call_anthropic(cls, person_dict: Dict[str, Any]) -> ProfileAnalysis:
        from backend import config
        try:
            prompt = cls._build_analysis_prompt(person_dict)
            headers = {
                "x-api-key": config.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            payload = {
                "model": "claude-3-haiku-20240307",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": f"{prompt}\nReturn pure JSON only."}]
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data["content"][0]["text"]
                    json_str = text.strip()
                    if "```json" in json_str:
                        json_str = json_str.split("```json")[1].split("```")[0].strip()
                    elif "```" in json_str:
                        json_str = json_str.split("```")[1].split("```")[0].strip()
                    content = json.loads(json_str)
                    content["analysis_engine"] = "llm_anthropic"
                    content["analyzed_at"] = datetime.now(timezone.utc).isoformat()
                    return ProfileAnalysis.model_validate(content)
                else:
                    logger.warning(f"Anthropic API returned status {resp.status_code}")
        except Exception as e:
            logger.warning(f"Anthropic analysis failed, falling back to deterministic: {type(e).__name__}")
        return cls.deterministic_analyze(person_dict)
        return cls.deterministic_analyze(person_dict)

    @classmethod
    def _build_analysis_prompt(cls, p: Dict[str, Any]) -> str:
        name = p.get("display_name", "")
        headline = cls.sanitize_untrusted_text(p.get("headline", ""))
        bio = cls.sanitize_untrusted_text(p.get("bio", ""))
        linkedin = p.get("linkedin_url", "")
        instagram = p.get("instagram_url", "")

        return f"""
Analyze the following public profile strictly based on verified evidence:
Name: {name}
Headline: {headline}
Bio/Summary: {bio}
LinkedIn: {linkedin}
Instagram: {instagram}

Requirements:
1. Do NOT hallucinate sensitive personal data (health, politics, religion, orientation).
2. Distinguish evidence-backed facts from missing/unknown dimensions.
3. Provide confidence score (0.0 to 1.0).

Return valid JSON with keys:
{{
  "summary": "Concise 2-sentence summary",
  "interests": ["list of strings"],
  "hobbies": ["list of strings"],
  "lifestyle_signals": ["list of strings"],
  "communication_style": "description string",
  "social_preferences": ["list of strings"],
  "compatibility_factors": ["list of strings"],
  "evidence_references": [
    {{"claim": "string", "source_url": "{linkedin}", "quote": "snippet", "confidence": 0.9}}
  ],
  "confidence_score": 0.92,
  "unknown_fields": ["list of unevidenced attributes"]
}}
"""
