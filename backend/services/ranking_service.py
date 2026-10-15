import uuid
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from backend.models import RankingItem
from backend.database import get_db

logger = logging.getLogger("ranking_service")

class RankingService:
    @classmethod
    def get_rankings_for_person(cls, target_person_id: str, limit: int = 25) -> List[RankingItem]:
        """Fetch ranked matches for a specific person with candidate profile details."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    r.id, r.target_person_id, r.candidate_person_id, r.rank,
                    r.score, r.mutual_score, r.primary_factors, r.dating_session_id,
                    p.display_name as candidate_name, p.headline as candidate_headline,
                    p.avatar_url as candidate_avatar, p.linkedin_url as candidate_linkedin_url,
                    p.instagram_url as candidate_instagram_url
                FROM compatibility_rankings r
                JOIN people p ON r.candidate_person_id = p.id
                WHERE r.target_person_id = ?
                ORDER BY r.score DESC, r.mutual_score DESC
                LIMIT ?
            """, (target_person_id, limit))
            
            rows = cursor.fetchall()

        results = []
        for idx, row in enumerate(rows):
            factors = []
            try:
                factors = json.loads(row["primary_factors"])
            except Exception:
                factors = ["High profile resonance"]

            results.append(RankingItem(
                id=row["id"],
                target_person_id=row["target_person_id"],
                candidate_person_id=row["candidate_person_id"],
                candidate_name=row["candidate_name"],
                candidate_headline=row["candidate_headline"],
                candidate_avatar=row["candidate_avatar"],
                candidate_linkedin_url=row["candidate_linkedin_url"],
                candidate_instagram_url=row["candidate_instagram_url"],
                rank=idx + 1,
                score=row["score"],
                mutual_score=row["mutual_score"],
                primary_factors=factors,
                dating_session_id=row["dating_session_id"]
            ))

        return results

    @classmethod
    def update_pair_ranking(
        cls, 
        target_id: str, 
        candidate_id: str, 
        score: float, 
        factors: List[str], 
        session_id: Optional[str] = None
    ) -> None:
        """Update or insert pair ranking safely with mutual verification."""
        now_str = datetime.now(timezone.utc).isoformat()
        with get_db() as conn:
            cursor = conn.cursor()
            ranking_id = f"rank_{target_id}_{candidate_id}"
            cursor.execute("""
                INSERT INTO compatibility_rankings (
                    id, target_person_id, candidate_person_id, rank, score,
                    mutual_score, primary_factors, dating_session_id, updated_at
                ) VALUES (?, ?, ?, 1, ?, ?, ?, ?, ?)
                ON CONFLICT(target_person_id, candidate_person_id) DO UPDATE SET
                    score = excluded.score,
                    mutual_score = excluded.mutual_score,
                    primary_factors = excluded.primary_factors,
                    dating_session_id = excluded.dating_session_id,
                    updated_at = excluded.updated_at
            """, (
                ranking_id, target_id, candidate_id, score, score,
                json.dumps(factors), session_id, now_str
            ))

            # Recalculate dynamic ranks for this target
            cursor.execute("""
                SELECT id FROM compatibility_rankings
                WHERE target_person_id = ?
                ORDER BY score DESC, mutual_score DESC
            """, (target_id,))
            rows = cursor.fetchall()
            for rank_num, r in enumerate(rows, start=1):
                cursor.execute("""
                    UPDATE compatibility_rankings SET rank = ? WHERE id = ?
                """, (rank_num, r["id"]))

    @classmethod
    def compute_all_rankings_if_empty(cls) -> None:
        """
        Compute baseline mutual compatibility rankings across all registered people
        if no rankings exist yet.
        """
        from backend.services.dating_service import AgentDatingEngine

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM compatibility_rankings")
            count = cursor.fetchone()["count"]
            if count > 0:
                return  # Already computed

            cursor.execute("SELECT * FROM people")
            people_rows = cursor.fetchall()

        if len(people_rows) < 2:
            return

        people = []
        with get_db() as conn:
            cursor = conn.cursor()
            for r in people_rows:
                p_dict = dict(r)
                cursor.execute("SELECT * FROM profile_analyses WHERE person_id = ?", (p_dict["id"],))
                ana = cursor.fetchone()
                if ana:
                    p_dict["analysis"] = {
                        "interests": json.loads(ana["interests"]),
                        "hobbies": json.loads(ana["hobbies"]),
                        "lifestyle_signals": json.loads(ana["lifestyle_signals"]),
                        "communication_style": ana["communication_style"],
                        "confidence_score": ana["confidence_score"]
                    }
                people.append(p_dict)

        # Compute pairwise compatibility matrix
        for i in range(len(people)):
            for j in range(i + 1, len(people)):
                p1 = people[i]
                p2 = people[j]
                score, breakdown, factors = AgentDatingEngine.compute_compatibility_breakdown(p1, p2)
                cls.update_pair_ranking(p1["id"], p2["id"], score, factors)
                cls.update_pair_ranking(p2["id"], p1["id"], score, factors)
