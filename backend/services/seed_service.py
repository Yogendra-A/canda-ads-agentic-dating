import json
import logging
from typing import Dict, Any
from datetime import datetime, timezone
from backend.database import get_db, init_db
from backend.services.demo_data import VERIFIED_PEOPLE_DATA
from backend.services.dating_service import AgentDatingEngine
from backend.services.ranking_service import RankingService

logger = logging.getLogger("seed_service")

# Curated pair matchups for precomputed demo interactions
PRECOMPUTED_PAIRS = [
    ("person_01", "person_24"),  # Reid Hoffman & Padmasree Warrior (Philosopher-technologist & Artist-reader)
    ("person_02", "person_04"),  # Satya Nadella & Andrew Ng (Empathetic leader & Dedicated AI educator)
    ("person_03", "person_09"),  # Sara Blakely & Alexis Ohanian (Inventive humor creator & Sports/Gaming dad)
    ("person_10", "person_11"),  # Melanie Perkins & Brian Chesky (Design democratizer & Architectural aesthete)
    ("person_06", "person_23"),  # Marques Brownlee & Tony Fadell (Matte-black gear craftsman & Hardware legend)
    ("person_05", "person_07"),  # Mira Murati & Lex Fridman (Classical piano engineer & Romantic martial artist)
    ("person_08", "person_22"),  # Tim Ferriss & Arianna Huffington (Biohacking experimentalist & Sleep/Thrive pioneer)
    ("person_16", "person_13"),  # Whitney Wolfe Herd & Guy Raz (Relationship founder & Empathetic storyteller)
    ("person_17", "person_25"),  # Dharmesh Shah & Jimmy Wales (Introverted coder & Open knowledge founder)
    ("person_14", "person_19"),  # Kara Swisher & Gary Vaynerchuk (Fearless interviewer & High-energy sports marketer)
    ("person_15", "person_20"),  # Jensen Huang & Gwyneth Paltrow (Accelerated computing cook & Wellness culinary curator)
    ("person_12", "person_21"),  # Reshma Saujani & Sam Altman (Bravery activist & Future energy/AGI visionary)
]

def seed_database(force_reseed: bool = False) -> Dict[str, Any]:
    """
    Seed 25 verified people, raw evidence sources, profile analyses,
    precomputed agent dating sessions, and complete mutual compatibility rankings.
    """
    init_db()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM people")
        existing_count = cursor.fetchone()["count"]

        if existing_count >= 25 and not force_reseed:
            logger.info("Database already seeded with verified dataset.")
            return {"status": "already_seeded", "people_count": existing_count}

        if force_reseed:
            cursor.execute("DELETE FROM dating_turns")
            cursor.execute("DELETE FROM dating_sessions")
            cursor.execute("DELETE FROM compatibility_rankings")
            cursor.execute("DELETE FROM profile_analyses")
            cursor.execute("DELETE FROM source_records")
            cursor.execute("DELETE FROM people")

        now_str = datetime.now(timezone.utc).isoformat()

        # 1. Insert 25 Verified People
        for p in VERIFIED_PEOPLE_DATA:
            cursor.execute("""
                INSERT OR REPLACE INTO people (
                    id, display_name, headline, bio, linkedin_url,
                    instagram_url, avatar_url, collection_method,
                    collection_timestamp, is_verified, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["id"], p["display_name"], p.get("headline"), p.get("bio"),
                p["linkedin_url"], p["instagram_url"], p.get("avatar_url"),
                p["collection_method"], now_str, 1, now_str, now_str
            ))

            # 2. Insert Source Records (Raw evidence & provenance)
            cursor.execute("""
                INSERT OR REPLACE INTO source_records (
                    id, person_id, source_platform, profile_url, raw_data,
                    retrieved_at, provenance
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"src_li_{p['id']}", p["id"], "linkedin", p["linkedin_url"],
                json.dumps({"headline": p.get("headline"), "verified": True}),
                now_str, "official_verified_public_profile"
            ))

            cursor.execute("""
                INSERT OR REPLACE INTO source_records (
                    id, person_id, source_platform, profile_url, raw_data,
                    retrieved_at, provenance
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"src_ig_{p['id']}", p["id"], "instagram", p["instagram_url"],
                json.dumps({"bio": p.get("bio"), "verified": True}),
                now_str, "official_verified_public_profile"
            ))

            # 3. Insert Profile Analysis
            ana = p["analysis"]
            cursor.execute("""
                INSERT OR REPLACE INTO profile_analyses (
                    id, person_id, summary, interests, hobbies, lifestyle_signals,
                    communication_style, social_preferences, compatibility_factors,
                    evidence_references, confidence_score, unknown_fields,
                    analysis_engine, analyzed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"ana_{p['id']}", p["id"], ana["summary"],
                json.dumps(ana["interests"]), json.dumps(ana["hobbies"]),
                json.dumps(ana["lifestyle_signals"]), ana["communication_style"],
                json.dumps(ana["social_preferences"]), json.dumps(ana["compatibility_factors"]),
                json.dumps([ref if isinstance(ref, dict) else ref.model_dump() for ref in ana["evidence_references"]]),
                ana["confidence_score"], json.dumps(ana["unknown_fields"]),
                ana["analysis_engine"], now_str
            ))

    # 4. Generate Precomputed Dating Sessions
    created_sessions_count = 0
    for p_a, p_b in PRECOMPUTED_PAIRS:
        try:
            AgentDatingEngine.run_dating_session(p_a, p_b, turns_count=6)
            created_sessions_count += 1
        except Exception as e:
            logger.warning(f"Error seeding pair {p_a}-{p_b}: {e}")

    # 5. Populate Complete Mutual Rankings for All 25 People
    RankingService.compute_all_rankings_if_empty()

    logger.info(f"Database successfully seeded with 25 people and {created_sessions_count} dating sessions.")
    return {
        "status": "seeded",
        "people_count": len(VERIFIED_PEOPLE_DATA),
        "sessions_count": created_sessions_count
    }
