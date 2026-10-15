from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator

class EvidenceItem(BaseModel):
    claim: str
    source_url: str
    quote: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)

class ProfileAnalysis(BaseModel):
    summary: str
    interests: List[str] = Field(default_factory=list)
    hobbies: List[str] = Field(default_factory=list)
    lifestyle_signals: List[str] = Field(default_factory=list)
    communication_style: str = "Evidence indicates thoughtful and engaging communication"
    social_preferences: List[str] = Field(default_factory=list)
    compatibility_factors: List[str] = Field(default_factory=list)
    evidence_references: List[EvidenceItem] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.85)
    unknown_fields: List[str] = Field(default_factory=list)
    analysis_engine: str = "deterministic_fallback"
    analyzed_at: str = ""

class PersonBase(BaseModel):
    display_name: str = Field(min_length=2)
    headline: Optional[str] = None
    bio: Optional[str] = None
    linkedin_url: str
    instagram_url: str
    avatar_url: Optional[str] = None
    collection_method: str = "manual_import" # 'apify_scrape', 'manual_import', 'verified_seed'
    is_verified: bool = True

    @field_validator("linkedin_url")
    def validate_linkedin(cls, v: str) -> str:
        v_clean = v.strip()
        if not ("linkedin.com/" in v_clean or "linkedin.com/in/" in v_clean):
            raise ValueError("Must be a valid LinkedIn profile URL (e.g., https://www.linkedin.com/in/username)")
        return v_clean

    @field_validator("instagram_url")
    def validate_instagram(cls, v: str) -> str:
        v_clean = v.strip()
        if not ("instagram.com/" in v_clean):
            raise ValueError("Must be a valid Instagram profile URL (e.g., https://www.instagram.com/username)")
        return v_clean

class PersonCreate(PersonBase):
    id: Optional[str] = None

class Person(PersonBase):
    id: str
    collection_timestamp: str
    created_at: str
    updated_at: str
    analysis: Optional[ProfileAnalysis] = None

class CompatibilityBreakdown(BaseModel):
    shared_interests: float = Field(ge=0, le=100)
    lifestyle_harmony: float = Field(ge=0, le=100)
    communication_resonance: float = Field(ge=0, le=100)
    mutual_curiosity: float = Field(ge=0, le=100)
    data_confidence: float = Field(ge=0, le=100)

class DatingTurn(BaseModel):
    id: str
    session_id: str
    turn_index: int
    speaker_id: str
    speaker_name: Optional[str] = None
    receiver_id: str
    receiver_name: Optional[str] = None
    message: str
    internal_reasoning: str
    compatibility_signals: List[str] = Field(default_factory=list)
    turn_sentiment: str = "warm"
    created_at: str

class DatingSession(BaseModel):
    id: str
    person_a_id: str
    person_a_name: Optional[str] = None
    person_a_avatar: Optional[str] = None
    person_b_id: str
    person_b_name: Optional[str] = None
    person_b_avatar: Optional[str] = None
    status: str = "completed"
    total_turns: int = 0
    overall_score: float = 0.0
    breakdown: CompatibilityBreakdown
    outcome_summary: str
    simulation_disclaimer: str = (
        "SIMULATED AGENT INTERACTION: This conversation was conducted autonomously by AI agents "
        "representing public profile data. It does NOT represent messages sent or received by real persons."
    )
    turns: List[DatingTurn] = Field(default_factory=list)
    created_at: str
    completed_at: Optional[str] = None

class RankingItem(BaseModel):
    id: str
    target_person_id: str
    candidate_person_id: str
    candidate_name: str
    candidate_headline: Optional[str] = None
    candidate_avatar: Optional[str] = None
    candidate_linkedin_url: str
    candidate_instagram_url: str
    rank: int
    score: float
    mutual_score: float
    primary_factors: List[str] = Field(default_factory=list)
    dating_session_id: Optional[str] = None

class DatingRunRequest(BaseModel):
    person_a_id: str
    person_b_id: str
    turns_count: int = Field(default=6, ge=2, le=10)

class ImportPersonItem(BaseModel):
    display_name: str
    headline: Optional[str] = None
    bio: Optional[str] = None
    linkedin_url: str
    instagram_url: str
    avatar_url: Optional[str] = None
    interests: Optional[List[str]] = None
    hobbies: Optional[List[str]] = None
    lifestyle_signals: Optional[List[str]] = None
    evidence_quote: Optional[str] = None

class ImportPayload(BaseModel):
    people: List[ImportPersonItem]

class CollectionStartRequest(BaseModel):
    actor_id: Optional[str] = None
    platform: Optional[str] = "both"  # 'linkedin' | 'instagram' | 'both'
    profile_urls: Optional[List[str]] = None

class SettingsUpdate(BaseModel):
    apify_api_token: Optional[str] = None
    apify_linkedin_actor_id: Optional[str] = None
    apify_instagram_actor_id: Optional[str] = None
    llm_provider: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

class SettingsResponse(BaseModel):
    has_apify_token: bool
    apify_linkedin_actor_id: str
    apify_instagram_actor_id: str
    llm_provider: str
    has_llm_key: bool
