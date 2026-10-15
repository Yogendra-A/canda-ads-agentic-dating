import os
import json
import uuid
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from backend.config import (
    CORS_ORIGINS, APIFY_API_TOKEN, APIFY_LINKEDIN_ACTOR_ID, APIFY_INSTAGRAM_ACTOR_ID,
    LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
)
from backend.database import init_db, get_db
from backend.models import (
    Person, PersonCreate, ProfileAnalysis, DatingSession, DatingTurn,
    RankingItem, DatingRunRequest, ImportPayload, CollectionStartRequest,
    SettingsResponse, SettingsUpdate
)
from backend.services.apify_service import ApifyService
from backend.services.analysis_service import ProfileAnalysisService
from backend.services.dating_service import AgentDatingEngine
from backend.services.ranking_service import RankingService
from backend.services.seed_service import seed_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(
    title="Canda Ads Agentic Dating Platform API",
    description="Autonomous AI Agent-to-Agent Dating, Compatibility Ranking & Public Profile Analysis Engine",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """Initialize database and seed baseline dataset if empty."""
    init_db()
    seed_database(force_reseed=False)

# 1. Health check
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "canda-ads-agentic-dating",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# 2. People Directory
@app.get("/api/people")
def get_people(
    search: Optional[str] = Query(None, description="Search by name, headline, or interests"),
    collection_method: Optional[str] = Query(None, description="Filter by collection method"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM people WHERE 1=1"
        params = []

        if collection_method:
            query += " AND collection_method = ?"
            params.append(collection_method)

        if search:
            query += " AND (display_name LIKE ? OR headline LIKE ? OR bio LIKE ?)"
            s_term = f"%{search}%"
            params.extend([s_term, s_term, s_term])

        query += " ORDER BY created_at ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()

        people_list = []
        for r in rows:
            p_dict = dict(r)
            # Fetch analysis
            cursor.execute("SELECT * FROM profile_analyses WHERE person_id = ?", (p_dict["id"],))
            ana = cursor.fetchone()
            if ana:
                p_dict["analysis"] = {
                    "summary": ana["summary"],
                    "interests": json.loads(ana["interests"]),
                    "hobbies": json.loads(ana["hobbies"]),
                    "lifestyle_signals": json.loads(ana["lifestyle_signals"]),
                    "communication_style": ana["communication_style"],
                    "social_preferences": json.loads(ana["social_preferences"]),
                    "compatibility_factors": json.loads(ana["compatibility_factors"]),
                    "evidence_references": json.loads(ana["evidence_references"]),
                    "confidence_score": ana["confidence_score"],
                    "unknown_fields": json.loads(ana["unknown_fields"]),
                    "analysis_engine": ana["analysis_engine"],
                    "analyzed_at": ana["analyzed_at"]
                }
            people_list.append(p_dict)

        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM people")
        total = cursor.fetchone()["total"]

        return {
            "total": total,
            "count": len(people_list),
            "people": people_list
        }

# 3. Person Detail
@app.get("/api/people/{person_id}")
def get_person(person_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people WHERE id = ?", (person_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Person not found")

        p_dict = dict(row)

        # Fetch analysis
        cursor.execute("SELECT * FROM profile_analyses WHERE person_id = ?", (person_id,))
        ana = cursor.fetchone()
        if ana:
            p_dict["analysis"] = {
                "summary": ana["summary"],
                "interests": json.loads(ana["interests"]),
                "hobbies": json.loads(ana["hobbies"]),
                "lifestyle_signals": json.loads(ana["lifestyle_signals"]),
                "communication_style": ana["communication_style"],
                "social_preferences": json.loads(ana["social_preferences"]),
                "compatibility_factors": json.loads(ana["compatibility_factors"]),
                "evidence_references": json.loads(ana["evidence_references"]),
                "confidence_score": ana["confidence_score"],
                "unknown_fields": json.loads(ana["unknown_fields"]),
                "analysis_engine": ana["analysis_engine"],
                "analyzed_at": ana["analyzed_at"]
            }

        # Fetch source records
        cursor.execute("SELECT * FROM source_records WHERE person_id = ?", (person_id,))
        src_rows = cursor.fetchall()
        p_dict["source_records"] = [dict(s) for s in src_rows]

        # Fetch top rankings for this person
        p_dict["rankings"] = [r.model_dump() for r in RankingService.get_rankings_for_person(person_id, limit=5)]

        # Fetch dating history
        cursor.execute("""
            SELECT s.*, 
                   pa.display_name as person_a_name, pa.avatar_url as person_a_avatar,
                   pb.display_name as person_b_name, pb.avatar_url as person_b_avatar
            FROM dating_sessions s
            JOIN people pa ON s.person_a_id = pa.id
            JOIN people pb ON s.person_b_id = pb.id
            WHERE s.person_a_id = ? OR s.person_b_id = ?
            ORDER BY s.created_at DESC LIMIT 10
        """, (person_id, person_id))
        sessions_rows = cursor.fetchall()
        p_dict["dating_history"] = []
        for s in sessions_rows:
            p_dict["dating_history"].append({
                "id": s["id"],
                "person_a_id": s["person_a_id"],
                "person_a_name": s["person_a_name"],
                "person_a_avatar": s["person_a_avatar"],
                "person_b_id": s["person_b_id"],
                "person_b_name": s["person_b_name"],
                "person_b_avatar": s["person_b_avatar"],
                "overall_score": s["overall_score"],
                "outcome_summary": s["outcome_summary"],
                "created_at": s["created_at"]
            })

        return p_dict

# 4. Import Profiles (CSV / JSON)
@app.post("/api/people/import")
def import_people(payload: ImportPayload):
    imported_count = 0
    now_str = datetime.now(timezone.utc).isoformat()

    with get_db() as conn:
        cursor = conn.cursor()
        for item in payload.people:
            person_id = f"person_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
                INSERT OR REPLACE INTO people (
                    id, display_name, headline, bio, linkedin_url,
                    instagram_url, avatar_url, collection_method,
                    collection_timestamp, is_verified, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                person_id, item.display_name, item.headline, item.bio,
                item.linkedin_url, item.instagram_url, item.avatar_url,
                "manual_import", now_str, 0, now_str, now_str
            ))

            # Automatically run profile analysis for newly imported person
            p_dict = {
                "id": person_id,
                "display_name": item.display_name,
                "headline": item.headline or "",
                "bio": item.bio or "",
                "linkedin_url": item.linkedin_url,
                "instagram_url": item.instagram_url
            }
            ana = ProfileAnalysisService.deterministic_analyze(p_dict)
            cursor.execute("""
                INSERT OR REPLACE INTO profile_analyses (
                    id, person_id, summary, interests, hobbies, lifestyle_signals,
                    communication_style, social_preferences, compatibility_factors,
                    evidence_references, confidence_score, unknown_fields,
                    analysis_engine, analyzed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"ana_{person_id}", person_id, ana.summary,
                json.dumps(ana.interests), json.dumps(ana.hobbies),
                json.dumps(ana.lifestyle_signals), ana.communication_style,
                json.dumps(ana.social_preferences), json.dumps(ana.compatibility_factors),
                json.dumps([ref.model_dump() for ref in ana.evidence_references]),
                ana.confidence_score, json.dumps(ana.unknown_fields),
                ana.analysis_engine, now_str
            ))
            imported_count += 1

    return {
        "status": "success",
        "imported_count": imported_count,
        "message": f"Imported {imported_count} profiles. Manual imports remain unverified until their identities and source URLs are checked."
    }

# 5. Apify Collection Trigger
@app.post("/api/collection/start")
async def start_collection(req: CollectionStartRequest):
    service = ApifyService()
    if not service.is_configured():
        raise HTTPException(
            status_code=400,
            detail="APIFY_API_TOKEN is not configured. Please supply an API key in Settings or use JSON/CSV import."
        )

    actor_id = req.actor_id or APIFY_LINKEDIN_ACTOR_ID
    try:
        run_data = await service.start_actor_run(
            actor_id=actor_id,
            run_input={"urls": req.profile_urls or []}
        )
        run_id = run_data.get("id", str(uuid.uuid4()))
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO collection_runs (
                    id, status, actor_id, platform, started_at
                ) VALUES (?, ?, ?, ?, ?)
            """, (run_id, "running", actor_id, req.platform or "linkedin", datetime.now(timezone.utc).isoformat()))
        return {
            "status": "started",
            "run_id": run_id,
            "actor_id": actor_id
        }
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

# 6. Apify Collection Status
@app.get("/api/collection/status/{run_id}")
async def get_collection_status(run_id: str):
    service = ApifyService()
    if not service.is_configured():
        return {"status": "unconfigured", "run_id": run_id, "error": "No API token configured."}

    try:
        run_data = await service.poll_actor_run(run_id)
        return {
            "run_id": run_id,
            "status": run_data.get("status", "UNKNOWN"),
            "dataset_id": run_data.get("defaultDatasetId")
        }
    except Exception as e:
        return {"run_id": run_id, "status": "error", "message": str(e)}

# 7. Analyze Person Profile
@app.post("/api/people/{person_id}/analyze")
async def analyze_person(person_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people WHERE id = ?", (person_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Person not found")

        p_dict = dict(row)

    analysis = await ProfileAnalysisService.analyze_with_llm(p_dict)
    now_str = datetime.now(timezone.utc).isoformat()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO profile_analyses (
                id, person_id, summary, interests, hobbies, lifestyle_signals,
                communication_style, social_preferences, compatibility_factors,
                evidence_references, confidence_score, unknown_fields,
                analysis_engine, analyzed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"ana_{person_id}", person_id, analysis.summary,
            json.dumps(analysis.interests), json.dumps(analysis.hobbies),
            json.dumps(analysis.lifestyle_signals), analysis.communication_style,
            json.dumps(analysis.social_preferences), json.dumps(analysis.compatibility_factors),
            json.dumps([ref.model_dump() for ref in analysis.evidence_references]),
            analysis.confidence_score, json.dumps(analysis.unknown_fields),
            analysis.analysis_engine, now_str
        ))

    return analysis

# 8. Batch Analyze All Unanalyzed Profiles
@app.post("/api/analysis/run")
def run_batch_analysis():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.* FROM people p
            LEFT JOIN profile_analyses a ON p.id = a.person_id
            WHERE a.id IS NULL
        """)
        unresolved = cursor.fetchall()

    count = 0
    now_str = datetime.now(timezone.utc).isoformat()
    for row in unresolved:
        p_dict = dict(row)
        ana = ProfileAnalysisService.deterministic_analyze(p_dict)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO profile_analyses (
                    id, person_id, summary, interests, hobbies, lifestyle_signals,
                    communication_style, social_preferences, compatibility_factors,
                    evidence_references, confidence_score, unknown_fields,
                    analysis_engine, analyzed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"ana_{p_dict['id']}", p_dict["id"], ana.summary,
                json.dumps(ana.interests), json.dumps(ana.hobbies),
                json.dumps(ana.lifestyle_signals), ana.communication_style,
                json.dumps(ana.social_preferences), json.dumps(ana.compatibility_factors),
                json.dumps([ref.model_dump() for ref in ana.evidence_references]),
                ana.confidence_score, json.dumps(ana.unknown_fields),
                ana.analysis_engine, now_str
            ))
            count += 1

    return {"status": "success", "analyzed_count": count}

# 9. Run Dating Session
@app.post("/api/dating/run")
def run_dating(req: DatingRunRequest):
    if req.person_a_id == req.person_b_id:
        raise HTTPException(status_code=400, detail="Cannot pair an agent with themselves.")

    try:
        session = AgentDatingEngine.run_dating_session(
            person_a_id=req.person_a_id,
            person_b_id=req.person_b_id,
            turns_count=req.turns_count
        )
        return session
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Dating session failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dating simulation error: {str(e)}")

# 10. List Dating Sessions
@app.get("/api/dating/sessions")
def get_dating_sessions(limit: int = 50):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, 
                   pa.display_name as person_a_name, pa.avatar_url as person_a_avatar,
                   pb.display_name as person_b_name, pb.avatar_url as person_b_avatar
            FROM dating_sessions s
            JOIN people pa ON s.person_a_id = pa.id
            JOIN people pb ON s.person_b_id = pb.id
            ORDER BY s.created_at DESC LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()

    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "person_a_id": r["person_a_id"],
            "person_a_name": r["person_a_name"],
            "person_a_avatar": r["person_a_avatar"],
            "person_b_id": r["person_b_id"],
            "person_b_name": r["person_b_name"],
            "person_b_avatar": r["person_b_avatar"],
            "status": r["status"],
            "total_turns": r["total_turns"],
            "overall_score": r["overall_score"],
            "breakdown": json.loads(r["breakdown"]),
            "outcome_summary": r["outcome_summary"],
            "simulation_disclaimer": r["simulation_disclaimer"],
            "created_at": r["created_at"],
            "completed_at": r["completed_at"]
        })
    return results

# 11. Get Dating Session Detail with Turns
@app.get("/api/dating/sessions/{session_id}")
def get_dating_session(session_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, 
                   pa.display_name as person_a_name, pa.avatar_url as person_a_avatar,
                   pb.display_name as person_b_name, pb.avatar_url as person_b_avatar
            FROM dating_sessions s
            JOIN people pa ON s.person_a_id = pa.id
            JOIN people pb ON s.person_b_id = pb.id
            WHERE s.id = ?
        """, (session_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Dating session not found")

        cursor.execute("""
            SELECT t.*, 
                   sp.display_name as speaker_name,
                   rc.display_name as receiver_name
            FROM dating_turns t
            JOIN people sp ON t.speaker_id = sp.id
            JOIN people rc ON t.receiver_id = rc.id
            WHERE t.session_id = ?
            ORDER BY t.turn_index ASC
        """, (session_id,))
        turn_rows = cursor.fetchall()

    turns = []
    for t in turn_rows:
        signals = []
        try:
            signals = json.loads(t["compatibility_signals"])
        except Exception:
            pass

        turns.append({
            "id": t["id"],
            "session_id": t["session_id"],
            "turn_index": t["turn_index"],
            "speaker_id": t["speaker_id"],
            "speaker_name": t["speaker_name"],
            "receiver_id": t["receiver_id"],
            "receiver_name": t["receiver_name"],
            "message": t["message"],
            "internal_reasoning": t["internal_reasoning"],
            "compatibility_signals": signals,
            "turn_sentiment": t["turn_sentiment"],
            "created_at": t["created_at"]
        })

    return {
        "id": row["id"],
        "person_a_id": row["person_a_id"],
        "person_a_name": row["person_a_name"],
        "person_a_avatar": row["person_a_avatar"],
        "person_b_id": row["person_b_id"],
        "person_b_name": row["person_b_name"],
        "person_b_avatar": row["person_b_avatar"],
        "status": row["status"],
        "total_turns": row["total_turns"],
        "overall_score": row["overall_score"],
        "breakdown": json.loads(row["breakdown"]),
        "outcome_summary": row["outcome_summary"],
        "simulation_disclaimer": row["simulation_disclaimer"],
        "created_at": row["created_at"],
        "completed_at": row["completed_at"],
        "turns": turns
    }

# 12. Personalized Rankings for Person
@app.get("/api/rankings/{person_id}")
def get_rankings(person_id: str, limit: int = 25):
    rankings = RankingService.get_rankings_for_person(person_id, limit=limit)
    return {
        "target_person_id": person_id,
        "count": len(rankings),
        "rankings": [r.model_dump() for r in rankings]
    }

# 13. Precomputed Demonstration Overview
@app.get("/api/demo")
def get_demo_overview():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as people_count FROM people")
        people_count = cursor.fetchone()["people_count"]

        cursor.execute("SELECT COUNT(*) as verified_count FROM people WHERE is_verified = 1")
        verified_count = cursor.fetchone()["verified_count"]

        cursor.execute("SELECT COUNT(*) as sessions_count FROM dating_sessions")
        sessions_count = cursor.fetchone()["sessions_count"]

        cursor.execute("SELECT COUNT(*) as analyzed_count FROM profile_analyses")
        analyzed_count = cursor.fetchone()["analyzed_count"]

        cursor.execute("""
            SELECT s.*, 
                   pa.display_name as person_a_name, pa.avatar_url as person_a_avatar,
                   pb.display_name as person_b_name, pb.avatar_url as person_b_avatar
            FROM dating_sessions s
            JOIN people pa ON s.person_a_id = pa.id
            JOIN people pb ON s.person_b_id = pb.id
            ORDER BY s.overall_score DESC LIMIT 6
        """)
        top_matches = cursor.fetchall()

    return {
        "dataset_complete": (people_count >= 25),
        "total_people": people_count,
        "verified_people": verified_count,
        "analyzed_profiles": analyzed_count,
        "completed_dating_sessions": sessions_count,
        "top_matches": [dict(m) for m in top_matches],
        "system_notice": (
            "Complete 25-person demonstration preloaded with verified public links, "
            "observable multi-turn agent dating transcripts, and mutual compatibility rankings."
        )
    }

# 14. Reset / Re-seed Demo Data
@app.post("/api/demo/seed")
def reseed_demo():
    result = seed_database(force_reseed=True)
    return {"status": "success", "result": result}

# 15. Settings & Config
@app.get("/api/settings")
def get_settings():
    from backend import config
    config.reload_config()
    return SettingsResponse(
        has_apify_token=bool(config.APIFY_API_TOKEN and config.APIFY_API_TOKEN.strip()),
        apify_linkedin_actor_id=config.APIFY_LINKEDIN_ACTOR_ID,
        apify_instagram_actor_id=config.APIFY_INSTAGRAM_ACTOR_ID,
        llm_provider=config.LLM_PROVIDER,
        has_llm_key=bool(config.OPENAI_API_KEY or config.ANTHROPIC_API_KEY or config.GEMINI_API_KEY)
    )

@app.post("/api/settings")
def update_settings(update: SettingsUpdate):
    from backend import config
    # Update active environment
    if update.apify_api_token is not None:
        os.environ["APIFY_API_TOKEN"] = update.apify_api_token
    if update.apify_linkedin_actor_id is not None:
        os.environ["APIFY_LINKEDIN_ACTOR_ID"] = update.apify_linkedin_actor_id
    if update.apify_instagram_actor_id is not None:
        os.environ["APIFY_INSTAGRAM_ACTOR_ID"] = update.apify_instagram_actor_id
    if update.llm_provider is not None:
        os.environ["LLM_PROVIDER"] = update.llm_provider
    if update.openai_api_key is not None:
        os.environ["OPENAI_API_KEY"] = update.openai_api_key
    if update.anthropic_api_key is not None:
        os.environ["ANTHROPIC_API_KEY"] = update.anthropic_api_key
    if update.gemini_api_key is not None:
        os.environ["GEMINI_API_KEY"] = update.gemini_api_key

    config.reload_config()
    return SettingsResponse(
        has_apify_token=bool(config.APIFY_API_TOKEN and config.APIFY_API_TOKEN.strip()),
        apify_linkedin_actor_id=config.APIFY_LINKEDIN_ACTOR_ID,
        apify_instagram_actor_id=config.APIFY_INSTAGRAM_ACTOR_ID,
        llm_provider=config.LLM_PROVIDER,
        has_llm_key=bool(config.OPENAI_API_KEY or config.ANTHROPIC_API_KEY or config.GEMINI_API_KEY)
    )

# Serve the Vite frontend from the same origin in production deployments.
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="frontend-assets")

    @app.get("/", include_in_schema=False)
    def serve_frontend_root():
        return FileResponse(FRONTEND_DIST / "index.html")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend_routes(full_path: str):
        # API and documentation paths must not fall back to the SPA.
        if full_path == "api" or full_path.startswith(("api/", "docs", "redoc", "openapi.json")):
            raise HTTPException(status_code=404, detail="Not found")
        candidate = (FRONTEND_DIST / full_path).resolve()
        if candidate.is_file() and FRONTEND_DIST.resolve() in candidate.parents:
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")
