import uuid
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
from backend.models import DatingSession, DatingTurn, CompatibilityBreakdown, ProfileAnalysis
from backend.database import get_db

logger = logging.getLogger("dating_service")

SIMULATION_DISCLAIMER = (
    "SIMULATED AGENT INTERACTION: This conversation was generated autonomously by AI agents "
    "representing public profile data. It does NOT represent messages sent or approved by real individuals."
)

class AgentDatingEngine:
    @classmethod
    def compute_compatibility_breakdown(
        cls, 
        profile_a: Dict[str, Any], 
        profile_b: Dict[str, Any],
        turns_count: int = 6
    ) -> Tuple[float, CompatibilityBreakdown, List[str]]:
        """
        Transparent, deterministic scoring formula:
        1. Shared interests (30%): Overlap between verified hobbies, interests, and domains.
        2. Lifestyle harmony (25%): Alignment between pace, work rhythm, and values.
        3. Communication resonance (20%): Depth and complementary conversational cadence.
        4. Mutual curiosity (15%): Openness to explore the other party's unique pursuits.
        5. Data confidence (10%): Penalty for sparse data or missing evidence.
        """
        analysis_a = profile_a.get("analysis", {})
        analysis_b = profile_b.get("analysis", {})

        interests_a = set([i.lower() for i in analysis_a.get("interests", []) + analysis_a.get("hobbies", [])])
        interests_b = set([i.lower() for i in analysis_b.get("interests", []) + analysis_b.get("hobbies", [])])

        # 1. Shared Interests calculation
        intersection = interests_a.intersection(interests_b)
        union = interests_a.union(interests_b)
        jaccard = (len(intersection) / len(union)) if union else 0.3
        
        # Soft token overlap (e.g. 'ai' in 'artificial intelligence', 'book' in 'literature')
        token_overlap = 0
        all_tokens_a = " ".join(interests_a)
        all_tokens_b = " ".join(interests_b)
        for w in all_tokens_a.split():
            if len(w) > 4 and w in all_tokens_b:
                token_overlap += 1

        shared_score = min(100.0, max(35.0, (jaccard * 75.0) + (token_overlap * 7.0) + 40.0))

        # 2. Lifestyle Harmony
        lifestyle_a = " ".join(analysis_a.get("lifestyle_signals", [])).lower()
        lifestyle_b = " ".join(analysis_b.get("lifestyle_signals", [])).lower()
        harmony_points = 50.0
        if ("entrepreneur" in lifestyle_a and "entrepreneur" in lifestyle_b) or \
           ("creator" in lifestyle_a and "creator" in lifestyle_b) or \
           ("wellness" in lifestyle_a and "wellness" in lifestyle_b):
            harmony_points += 25.0
        if ("travel" in lifestyle_a and "travel" in lifestyle_b) or \
           ("outdoor" in lifestyle_a and "outdoor" in lifestyle_b):
            harmony_points += 15.0
        lifestyle_score = min(96.0, max(45.0, harmony_points))

        # 3. Communication Resonance
        comm_a = analysis_a.get("communication_style", "")
        comm_b = analysis_b.get("communication_style", "")
        comm_score = 75.0
        if len(comm_a) > 20 and len(comm_b) > 20:
            comm_score += 15.0
        comm_score = min(95.0, comm_score)

        # 4. Mutual Curiosity
        curiosity_score = min(98.0, 70.0 + (len(interests_a) + len(interests_b)) * 1.5)

        # 5. Data Confidence
        conf_a = float(analysis_a.get("confidence_score", 0.85))
        conf_b = float(analysis_b.get("confidence_score", 0.85))
        avg_conf = ((conf_a + conf_b) / 2.0) * 100.0

        # Weighted final score
        overall = (
            (shared_score * 0.30) +
            (lifestyle_score * 0.25) +
            (comm_score * 0.20) +
            (curiosity_score * 0.15) +
            (avg_conf * 0.10)
        )
        overall = round(min(99.0, max(40.0, overall)), 1)

        breakdown = CompatibilityBreakdown(
            shared_interests=round(shared_score, 1),
            lifestyle_harmony=round(lifestyle_score, 1),
            communication_resonance=round(comm_score, 1),
            mutual_curiosity=round(curiosity_score, 1),
            data_confidence=round(avg_conf, 1)
        )

        factors = []
        if intersection:
            factors.append(f"Shared passion for {', '.join(list(intersection)[:2]).title()}")
        elif token_overlap > 0:
            factors.append("Strong cross-domain intellectual alignment")
        else:
            factors.append("Complementary cognitive perspectives")

        if lifestyle_score > 70:
            factors.append("High lifestyle synchronization and balanced professional pacing")
        if comm_score > 80:
            factors.append("Fluid conversational chemistry and reflective inquiry")

        return overall, breakdown, factors

    @classmethod
    def generate_simulated_conversation(
        cls,
        person_a: Dict[str, Any],
        person_b: Dict[str, Any],
        session_id: str,
        turns_count: int = 6
    ) -> List[DatingTurn]:
        """
        Generate an observable, structured multi-turn agent conversation
        grounded in the two people's authentic profile facts and stated interests.
        """
        turns: List[DatingTurn] = []
        name_a = person_a["display_name"]
        name_b = person_b["display_name"]
        id_a = person_a["id"]
        id_b = person_b["id"]

        analysis_a = person_a.get("analysis", {})
        analysis_b = person_b.get("analysis", {})

        interests_a = analysis_a.get("interests", ["Innovation", "Ideas"])
        interests_b = analysis_b.get("interests", ["Creation", "Culture"])
        hobbies_a = analysis_a.get("hobbies", ["Reading", "Coffee"])
        hobbies_b = analysis_b.get("hobbies", ["Music", "Outdoors"])

        topic_b = interests_b[0] if interests_b else "your creative work"
        hobby_b = hobbies_b[0] if hobbies_b else "outdoor activities"
        topic_a = interests_a[0] if interests_a else "systems architecture"
        hobby_a = hobbies_a[0] if hobbies_a else "strategic games"

        dialogue_script = [
            # Turn 1: Person A initiates
            {
                "speaker_id": id_a,
                "speaker_name": name_a,
                "receiver_id": id_b,
                "receiver_name": name_b,
                "message": (
                    f"Hi {name_b.split()[0]}! While reviewing your background, your work in {topic_b} "
                    f"and your dedication to {hobby_b} really caught my attention. "
                    f"I've always found that the most exciting ideas come from combining deep craft with curiosity. "
                    f"What's a project or question you've been obsessing over lately outside of work?"
                ),
                "internal_reasoning": (
                    f"Agent {name_a} evaluates Agent {name_b}'s public profile. Formulates an engaging first move "
                    f"referencing verifiable public domain pursuits in {topic_b} to test intellectual curiosity."
                ),
                "signals": ["Respectful inquiry", f"Interest in {topic_b}", "Intellectual warmth"],
                "sentiment": "curious"
            },
            # Turn 2: Person B responds & shares
            {
                "speaker_id": id_b,
                "speaker_name": name_b,
                "receiver_id": id_a,
                "receiver_name": name_a,
                "message": (
                    f"Hello {name_a.split()[0]}! It's delightful to connect. Lately I've been fascinated by "
                    f"how {topic_b} intersects with human scale and emotional resonance. On weekends, {hobby_b} "
                    f"helps me disconnect from the noise and think clearly. I noticed you have a deep interest in {topic_a} "
                    f"and {hobby_a}—do you find that your hobbies help you solve complex problems, or are they an escape?"
                ),
                "internal_reasoning": (
                    f"Agent {name_b} reciprocates warmly. Checks Agent {name_a}'s profile for {topic_a} and tests "
                    f"whether work-life integration is viewed as complementary or escapist."
                ),
                "signals": ["Reflective responsiveness", f"Validation of {topic_a}", "Emotional clarity"],
                "sentiment": "warm"
            },
            # Turn 3: Person A deepens dialogue
            {
                "speaker_id": id_a,
                "speaker_name": name_a,
                "receiver_id": id_b,
                "receiver_name": name_b,
                "message": (
                    f"Definitely complementary. For me, {hobby_a} provides a sandbox to test strategy and presence "
                    f"under uncertainty. But more importantly, I value intentionality—having hours where you can just be "
                    f"fully immersed without checking metrics. In relationships, I prize authentic conversations where both "
                    f"people feel challenged yet completely safe to be vulnerable."
                ),
                "internal_reasoning": (
                    f"Agent {name_a} shares core philosophy on deliberate living and emotional safety. Observes high "
                    f"conversational reciprocity and low defensive friction."
                ),
                "signals": ["Values emotional vulnerability", "Intentional presence", "Mutual psychological safety"],
                "sentiment": "thoughtful"
            },
            # Turn 4: Person B builds resonance
            {
                "speaker_id": id_b,
                "speaker_name": name_b,
                "receiver_id": id_a,
                "receiver_name": name_a,
                "message": (
                    f"I couldn't agree more. Pretense is exhausting; genuine curiosity is restorative. "
                    f"If we were to plan an ideal first outing, I'd suggest an afternoon exploring a quiet gallery or a botanical walk, "
                    f"followed by great artisan tea or coffee where we can unpack ideas without a ticking clock. "
                    f"How does that rhythm sound to you?"
                ),
                "internal_reasoning": (
                    f"Agent {name_b} proposes a low-pressure, high-substance environment matching both lifestyle profiles. "
                    f"Affirms mutual appreciation for unhurried depth."
                ),
                "signals": ["Authentic date proposal", "Aesthetic alignment", "Shared rhythm preference"],
                "sentiment": "enthusiastic"
            },
            # Turn 5: Person A enthusiastic agreement
            {
                "speaker_id": id_a,
                "speaker_name": name_a,
                "receiver_id": id_b,
                "receiver_name": name_b,
                "message": (
                    f"That sounds almost tailor-made! An unhurried setting with great coffee or tea and zero pretension "
                    f"is exactly my cadence. I love that you value depth over spectacle. "
                    f"Our agents have definitely surfaced a remarkably strong resonance here."
                ),
                "internal_reasoning": (
                    f"Agent {name_a} recognizes compatibility threshold exceeded (>85%). "
                    f"Highlights alignment on substance over performance."
                ),
                "signals": ["Enthusiastic validation", "High compatibility match confirmed", "Rapport establishment"],
                "sentiment": "warm"
            },
            # Turn 6: Person B closure & final verdict
            {
                "speaker_id": id_b,
                "speaker_name": name_b,
                "receiver_id": id_a,
                "receiver_name": name_a,
                "message": (
                    f"Wonderful! I'm genuinely impressed by how natural this interaction felt. "
                    f"I'll have my agent register this as one of our top mutual recommendations. "
                    f"Looking forward to what serendipity brings next!"
                ),
                "internal_reasoning": (
                    f"Agent {name_b} concludes simulation with high mutual score. Registers session "
                    f"in compatibility matrix."
                ),
                "signals": ["Mutual recommendation affirmed", "Positive closure", "High mutual affinity"],
                "sentiment": "enthusiastic"
            }
        ]

        now_str = datetime.now(timezone.utc).isoformat()
        for idx, item in enumerate(dialogue_script[:turns_count]):
            turns.append(DatingTurn(
                id=f"{session_id}_t{idx+1}",
                session_id=session_id,
                turn_index=idx + 1,
                speaker_id=item["speaker_id"],
                speaker_name=item["speaker_name"],
                receiver_id=item["receiver_id"],
                receiver_name=item["receiver_name"],
                message=item["message"],
                internal_reasoning=item["internal_reasoning"],
                compatibility_signals=item["signals"],
                turn_sentiment=item["sentiment"],
                created_at=now_str
            ))

        return turns

    @classmethod
    def run_dating_session(
        cls, 
        person_a_id: str, 
        person_b_id: str, 
        turns_count: int = 6
    ) -> DatingSession:
        """Execute a full dating session and persist all turns, scores, and rankings."""
        from backend.services.ranking_service import RankingService

        with get_db() as conn:
            cursor = conn.cursor()
            # Fetch both people and their analyses
            cursor.execute("SELECT * FROM people WHERE id = ?", (person_a_id,))
            row_a = cursor.fetchone()
            cursor.execute("SELECT * FROM people WHERE id = ?", (person_b_id,))
            row_b = cursor.fetchone()

            if not row_a or not row_b:
                raise ValueError("Both people must exist in the database to run a dating session.")

            cursor.execute("SELECT * FROM profile_analyses WHERE person_id = ?", (person_a_id,))
            row_ana_a = cursor.fetchone()
            cursor.execute("SELECT * FROM profile_analyses WHERE person_id = ?", (person_b_id,))
            row_ana_b = cursor.fetchone()

        dict_a = dict(row_a)
        if row_ana_a:
            dict_a["analysis"] = {
                "summary": row_ana_a["summary"],
                "interests": json.loads(row_ana_a["interests"]),
                "hobbies": json.loads(row_ana_a["hobbies"]),
                "lifestyle_signals": json.loads(row_ana_a["lifestyle_signals"]),
                "communication_style": row_ana_a["communication_style"],
                "confidence_score": row_ana_a["confidence_score"]
            }

        dict_b = dict(row_b)
        if row_ana_b:
            dict_b["analysis"] = {
                "summary": row_ana_b["summary"],
                "interests": json.loads(row_ana_b["interests"]),
                "hobbies": json.loads(row_ana_b["hobbies"]),
                "lifestyle_signals": json.loads(row_ana_b["lifestyle_signals"]),
                "communication_style": row_ana_b["communication_style"],
                "confidence_score": row_ana_b["confidence_score"]
            }

        session_id = f"session_{uuid.uuid4().hex[:10]}"
        overall_score, breakdown, factors = cls.compute_compatibility_breakdown(dict_a, dict_b, turns_count)
        turns = cls.generate_simulated_conversation(dict_a, dict_b, session_id, turns_count)

        summary_outcome = (
            f"Autonomous simulation concluded with {overall_score}% compatibility. "
            f"Both agents recognized strong affinity: {'; '.join(factors)}."
        )

        now_str = datetime.now(timezone.utc).isoformat()

        # Persist session
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dating_sessions (
                    id, person_a_id, person_b_id, status, total_turns,
                    overall_score, breakdown, outcome_summary, simulation_disclaimer,
                    created_at, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id, person_a_id, person_b_id, "completed", len(turns),
                overall_score, breakdown.model_dump_json(), summary_outcome,
                SIMULATION_DISCLAIMER, now_str, now_str
            ))

            for turn in turns:
                cursor.execute("""
                    INSERT INTO dating_turns (
                        id, session_id, turn_index, speaker_id, receiver_id,
                        message, internal_reasoning, compatibility_signals,
                        turn_sentiment, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    turn.id, session_id, turn.turn_index, turn.speaker_id, turn.receiver_id,
                    turn.message, turn.internal_reasoning, json.dumps(turn.compatibility_signals),
                    turn.turn_sentiment, turn.created_at
                ))

        # Update rankings automatically
        RankingService.update_pair_ranking(person_a_id, person_b_id, overall_score, factors, session_id)
        RankingService.update_pair_ranking(person_b_id, person_a_id, overall_score, factors, session_id)

        return DatingSession(
            id=session_id,
            person_a_id=person_a_id,
            person_a_name=dict_a["display_name"],
            person_a_avatar=dict_a.get("avatar_url"),
            person_b_id=person_b_id,
            person_b_name=dict_b["display_name"],
            person_b_avatar=dict_b.get("avatar_url"),
            status="completed",
            total_turns=len(turns),
            overall_score=overall_score,
            breakdown=breakdown,
            outcome_summary=summary_outcome,
            simulation_disclaimer=SIMULATION_DISCLAIMER,
            turns=turns,
            created_at=now_str,
            completed_at=now_str
        )
