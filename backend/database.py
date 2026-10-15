import sqlite3
import json
from contextlib import contextmanager
from typing import Generator, Any
from backend.config import DATABASE_PATH

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db() -> None:
    """Initialize database tables with optimal schema and indexes."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. People table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS people (
                id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                headline TEXT,
                bio TEXT,
                linkedin_url TEXT NOT NULL UNIQUE,
                instagram_url TEXT NOT NULL UNIQUE,
                avatar_url TEXT,
                collection_method TEXT NOT NULL,
                collection_timestamp TEXT NOT NULL,
                is_verified INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)

        # 2. Source records table (raw evidence & provenance)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS source_records (
                id TEXT PRIMARY KEY,
                person_id TEXT NOT NULL,
                source_platform TEXT NOT NULL,
                profile_url TEXT NOT NULL,
                raw_data TEXT NOT NULL,
                retrieved_at TEXT NOT NULL,
                provenance TEXT,
                FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
            );
        """)

        # 3. Profile analyses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile_analyses (
                id TEXT PRIMARY KEY,
                person_id TEXT NOT NULL UNIQUE,
                summary TEXT NOT NULL,
                interests TEXT NOT NULL,
                hobbies TEXT NOT NULL,
                lifestyle_signals TEXT NOT NULL,
                communication_style TEXT NOT NULL,
                social_preferences TEXT NOT NULL,
                compatibility_factors TEXT NOT NULL,
                evidence_references TEXT NOT NULL,
                confidence_score REAL NOT NULL,
                unknown_fields TEXT NOT NULL,
                analysis_engine TEXT NOT NULL,
                analyzed_at TEXT NOT NULL,
                FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
            );
        """)

        # 4. Dating sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dating_sessions (
                id TEXT PRIMARY KEY,
                person_a_id TEXT NOT NULL,
                person_b_id TEXT NOT NULL,
                status TEXT NOT NULL,
                total_turns INTEGER NOT NULL DEFAULT 0,
                overall_score REAL NOT NULL,
                breakdown TEXT NOT NULL,
                outcome_summary TEXT NOT NULL,
                simulation_disclaimer TEXT NOT NULL,
                created_at TEXT NOT NULL,
                completed_at TEXT,
                FOREIGN KEY (person_a_id) REFERENCES people(id) ON DELETE CASCADE,
                FOREIGN KEY (person_b_id) REFERENCES people(id) ON DELETE CASCADE
            );
        """)

        # 5. Dating turns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dating_turns (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                turn_index INTEGER NOT NULL,
                speaker_id TEXT NOT NULL,
                receiver_id TEXT NOT NULL,
                message TEXT NOT NULL,
                internal_reasoning TEXT NOT NULL,
                compatibility_signals TEXT NOT NULL,
                turn_sentiment TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES dating_sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (speaker_id) REFERENCES people(id) ON DELETE CASCADE,
                FOREIGN KEY (receiver_id) REFERENCES people(id) ON DELETE CASCADE
            );
        """)

        # 6. Compatibility rankings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compatibility_rankings (
                id TEXT PRIMARY KEY,
                target_person_id TEXT NOT NULL,
                candidate_person_id TEXT NOT NULL,
                rank INTEGER NOT NULL,
                score REAL NOT NULL,
                mutual_score REAL NOT NULL,
                primary_factors TEXT NOT NULL,
                dating_session_id TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (target_person_id) REFERENCES people(id) ON DELETE CASCADE,
                FOREIGN KEY (candidate_person_id) REFERENCES people(id) ON DELETE CASCADE,
                FOREIGN KEY (dating_session_id) REFERENCES dating_sessions(id) ON DELETE SET NULL,
                UNIQUE(target_person_id, candidate_person_id)
            );
        """)

        # 7. Collection runs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collection_runs (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                actor_id TEXT,
                platform TEXT,
                items_scraped INTEGER DEFAULT 0,
                items_imported INTEGER DEFAULT 0,
                error_message TEXT,
                started_at TEXT NOT NULL,
                completed_at TEXT
            );
        """)

        # Indexes for fast lookup
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_people_collection ON people(collection_method);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_dating_turns_session ON dating_turns(session_id, turn_index);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rankings_target ON compatibility_rankings(target_person_id, rank);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_source_records_person ON source_records(person_id);")
