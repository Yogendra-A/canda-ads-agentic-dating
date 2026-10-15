import pytest
import json
from pydantic import ValidationError
from backend.models import PersonCreate, ImportPayload, ImportPersonItem, ProfileAnalysis
from backend.services.apify_service import ApifyService
from backend.services.analysis_service import ProfileAnalysisService
from backend.services.dating_service import AgentDatingEngine
from backend.services.ranking_service import RankingService
from backend.services.seed_service import seed_database
from backend.database import init_db, get_db

@pytest.fixture(autouse=True)
def setup_test_db():
    init_db()
    seed_database(force_reseed=False)

# 1. Profile URL validation
def test_profile_url_validation_success():
    valid = PersonCreate(
        display_name="Test Person",
        linkedin_url="https://www.linkedin.com/in/testuser",
        instagram_url="https://www.instagram.com/testuser"
    )
    assert "linkedin.com/in/testuser" in valid.linkedin_url
    assert "instagram.com/testuser" in valid.instagram_url

def test_profile_url_validation_failure():
    with pytest.raises(ValidationError):
        PersonCreate(
            display_name="Bad Person",
            linkedin_url="https://facebook.com/fake",
            instagram_url="https://instagram.com/good"
        )

    with pytest.raises(ValidationError):
        PersonCreate(
            display_name="Bad Person",
            linkedin_url="https://linkedin.com/in/good",
            instagram_url="https://twitter.com/fake"
        )

# 2. Dataset import & deduplication
def test_dataset_import_validation():
    payload = ImportPayload(people=[
        ImportPersonItem(
            display_name="Imported Person",
            linkedin_url="https://www.linkedin.com/in/imported",
            instagram_url="https://www.instagram.com/imported",
            headline="Founder at TestLab"
        )
    ])
    assert len(payload.people) == 1
    assert payload.people[0].display_name == "Imported Person"

# 3. Apify response normalization
def test_apify_linkedin_normalization():
    raw_li = {
        "fullName": "Sarah Connor",
        "occupation": "Cybernetics Lead",
        "publicProfileUrl": "https://www.linkedin.com/in/sarah-connor",
        "skills": [{"name": "AI Safety"}, "Robotics"]
    }
    norm = ApifyService.normalize_linkedin_item(raw_li)
    assert norm["display_name"] == "Sarah Connor"
    assert norm["headline"] == "Cybernetics Lead"
    assert norm["profile_url"] == "https://www.linkedin.com/in/sarah-connor"
    assert "AI Safety" in norm["skills"]

def test_apify_instagram_private_rejection():
    raw_private_ig = {
        "username": "secret_user",
        "isPrivate": True
    }
    assert ApifyService.normalize_instagram_item(raw_private_ig) is None

def test_apify_instagram_public_normalization():
    raw_pub_ig = {
        "username": "public_creator",
        "fullName": "Public Creator",
        "biography": "Exploring photography and sound",
        "isPrivate": False,
        "latestPosts": [{"caption": "Sunset in Malibu"}]
    }
    norm = ApifyService.normalize_instagram_item(raw_pub_ig)
    assert norm is not None
    assert norm["username"] == "public_creator"
    assert len(norm["captions"]) == 1

# 4. Profile schema validation
def test_profile_analysis_schema():
    analysis = ProfileAnalysisService.deterministic_analyze({
        "display_name": "Ada Lovelace",
        "headline": "First Computer Programmer | Mathematics and Analytical Engine Pioneer",
        "bio": "Devoted to poetical science, mathematics, and early mechanical computation.",
        "linkedin_url": "https://www.linkedin.com/in/adalovelace",
        "instagram_url": "https://www.instagram.com/adalovelace"
    })
    assert analysis.summary is not None
    assert len(analysis.interests) > 0
    assert 0.0 <= analysis.confidence_score <= 1.0
    assert analysis.analysis_engine == "deterministic_fallback"

# 5. Compatibility score bounds and determinism
def test_compatibility_score_bounds_and_determinism():
    profile_a = {
        "id": "p_a",
        "display_name": "Person A",
        "analysis": {
            "interests": ["Artificial Intelligence", "Chess"],
            "hobbies": ["Reading"],
            "lifestyle_signals": ["High-agency pace"],
            "communication_style": "Reflective and deep",
            "confidence_score": 0.95
        }
    }
    profile_b = {
        "id": "p_b",
        "display_name": "Person B",
        "analysis": {
            "interests": ["Artificial Intelligence", "Philosophy"],
            "hobbies": ["Board games"],
            "lifestyle_signals": ["High-agency pace"],
            "communication_style": "Reflective and deep",
            "confidence_score": 0.92
        }
    }

    score1, breakdown1, _ = AgentDatingEngine.compute_compatibility_breakdown(profile_a, profile_b)
    score2, breakdown2, _ = AgentDatingEngine.compute_compatibility_breakdown(profile_a, profile_b)

    # Determinism
    assert score1 == score2
    assert breakdown1.shared_interests == breakdown2.shared_interests
    # Bounds
    assert 0.0 <= score1 <= 100.0
    assert 0.0 <= breakdown1.shared_interests <= 100.0
    assert 0.0 <= breakdown1.lifestyle_harmony <= 100.0

# 6. Mutual ranking generation
def test_mutual_ranking_generation():
    RankingService.update_pair_ranking("person_01", "person_02", 88.5, ["Shared intellectual stamina"])
    RankingService.update_pair_ranking("person_02", "person_01", 88.5, ["Shared intellectual stamina"])

    rankings_1 = RankingService.get_rankings_for_person("person_01")
    rankings_2 = RankingService.get_rankings_for_person("person_02")

    assert any(r.candidate_person_id == "person_02" for r in rankings_1)
    assert any(r.candidate_person_id == "person_01" for r in rankings_2)

# 7. Agent conversation turn limits
def test_agent_conversation_turn_limits():
    session = AgentDatingEngine.run_dating_session("person_01", "person_02", turns_count=4)
    assert len(session.turns) == 4
    assert session.turns[0].speaker_id == "person_01"
    assert session.turns[1].speaker_id == "person_02"
    assert "SIMULATED AGENT INTERACTION" in session.simulation_disclaimer

# 8. Missing-data handling
def test_missing_data_handling():
    # Empty profile attributes should not crash and should reflect lower confidence
    sparse_profile = {
        "display_name": "Minimalist",
        "headline": "",
        "bio": "",
        "linkedin_url": "https://www.linkedin.com/in/minimal",
        "instagram_url": "https://www.instagram.com/minimal"
    }
    ana = ProfileAnalysisService.deterministic_analyze(sparse_profile)
    assert len(ana.unknown_fields) > 0
    assert ana.summary != ""

# 9. Persistence across reloads
def test_persistence_across_reloads():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM people")
        count = cursor.fetchone()["count"]
        assert count >= 25

        cursor.execute("SELECT COUNT(*) as count FROM dating_sessions")
        sessions_count = cursor.fetchone()["count"]
        assert sessions_count > 0
