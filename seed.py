#!/usr/bin/env python3
"""
Seed script to initialize SQLite database with 25 verified public figures,
evidence sources, precomputed dating runs, and mutual rankings.
"""
import sys
from backend.database import init_db
from backend.services.seed_service import seed_database

def main():
    print("Initializing database tables...")
    init_db()
    print("Seeding 25 verified public figures, evidence citations, and precomputed dating sessions...")
    result = seed_database(force_reseed=True)
    print(f"Seed complete: {result}")

if __name__ == "__main__":
    main()
