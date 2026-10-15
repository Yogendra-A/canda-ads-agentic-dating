export interface EvidenceItem {
  claim: string;
  source_url: string;
  quote?: string;
  confidence: number;
}

export interface ProfileAnalysis {
  summary: string;
  interests: string[];
  hobbies: string[];
  lifestyle_signals: string[];
  communication_style: string;
  social_preferences: string[];
  compatibility_factors: string[];
  evidence_references: EvidenceItem[];
  confidence_score: number;
  unknown_fields: string[];
  analysis_engine: string;
  analyzed_at: string;
}

export interface Person {
  id: string;
  display_name: string;
  headline?: string;
  bio?: string;
  linkedin_url: string;
  instagram_url: string;
  avatar_url?: string;
  collection_method: string;
  collection_timestamp: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  analysis?: ProfileAnalysis;
  rankings?: RankingItem[];
  dating_history?: any[];
  source_records?: any[];
}

export interface CompatibilityBreakdown {
  shared_interests: number;
  lifestyle_harmony: number;
  communication_resonance: number;
  mutual_curiosity: number;
  data_confidence: number;
}

export interface DatingTurn {
  id: string;
  session_id: string;
  turn_index: number;
  speaker_id: string;
  speaker_name?: string;
  receiver_id: string;
  receiver_name?: string;
  message: string;
  internal_reasoning: string;
  compatibility_signals: string[];
  turn_sentiment: string;
  created_at: string;
}

export interface DatingSession {
  id: string;
  person_a_id: string;
  person_a_name?: string;
  person_a_avatar?: string;
  person_b_id: string;
  person_b_name?: string;
  person_b_avatar?: string;
  status: string;
  total_turns: number;
  overall_score: number;
  breakdown: CompatibilityBreakdown;
  outcome_summary: string;
  simulation_disclaimer: string;
  turns: DatingTurn[];
  created_at: string;
  completed_at?: string;
}

export interface RankingItem {
  id: string;
  target_person_id: string;
  candidate_person_id: string;
  candidate_name: string;
  candidate_headline?: string;
  candidate_avatar?: string;
  candidate_linkedin_url: string;
  candidate_instagram_url: string;
  rank: number;
  score: number;
  mutual_score: number;
  primary_factors: string[];
  dating_session_id?: string;
}

export interface DemoOverview {
  dataset_complete: boolean;
  total_people: number;
  verified_people: number;
  analyzed_profiles: number;
  completed_dating_sessions: number;
  top_matches: any[];
  system_notice: string;
}

export interface SettingsResponse {
  has_apify_token: boolean;
  apify_linkedin_actor_id: string;
  apify_instagram_actor_id: string;
  llm_provider: string;
  has_llm_key: boolean;
}
