# SQLite wrapper for storing user profile, preferences, and assessment results persistently.

import os
import sqlite3
import json

# Directory and file path for the SQLite database.
DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "app_data.db")

# Default values used when no saved profile exists.
_DEFAULTS = {
    "user_name": "",        # User's display name.
    "avatar_path": "",      # Path to the user's avatar image.
    "language": "fa",       # Preferred language code.
    "theme": "dark",        # Preferred theme ('dark' or 'light').
    "answers": None,        # JSON string: list of answer indexes from the last finished assessment.
    "skill_scores": None,   # JSON string: dict of skill -> score from the last finished assessment.
    "has_results": 0,       # Flag indicating if the user has completed an assessment (0 or 1).
}


def _connect():
    # Create the database directory if it doesn't exist.
    os.makedirs(DB_DIR, exist_ok=True)
    # Connect to the SQLite database.
    conn = sqlite3.connect(DB_PATH)
    # Create the profile table if it doesn't exist.
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            user_name TEXT,
            avatar_path TEXT,
            language TEXT,
            theme TEXT,
            answers TEXT,
            skill_scores TEXT,
            has_results INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    return conn


def load_profile():
    """Read the saved profile. Always returns a dict with every key present
    (falling back to defaults), so callers never need to check for missing
    keys."""
    try:
        # Connect to the database.
        conn = _connect()
        # Query the profile row with id=1 (only one row exists).
        cur = conn.execute(
            "SELECT user_name, avatar_path, language, theme, answers, skill_scores, has_results "
            "FROM profile WHERE id = 1"
        )
        row = cur.fetchone()
        conn.close()
        # If no profile exists, return the default values.
        if row is None:
            return dict(_DEFAULTS)
        # Start with defaults and update with the retrieved values.
        profile = dict(_DEFAULTS)
        profile.update({
            "user_name": row[0] or "",
            "avatar_path": row[1] or "",
            "language": row[2] or "fa",
            "theme": row[3] or "dark",
            "answers": row[4],
            "skill_scores": row[5],
            "has_results": row[6] or 0,
        })
        return profile
    except Exception:
        # If the database is corrupt or missing, behave as if it's the first run.
        return dict(_DEFAULTS)


def save_profile(**fields):
    """Update only the given fields (any subset of _DEFAULTS' keys), keeping
    everything else that was already saved. Creates the row on first use."""
    try:
        # Load the current profile and update with the new fields.
        current = load_profile()
        current.update(fields)
        # Connect to the database.
        conn = _connect()
        # Insert or replace the profile row.
        conn.execute(
            """
            INSERT INTO profile (id, user_name, avatar_path, language, theme, answers, skill_scores, has_results)
            VALUES (1, :user_name, :avatar_path, :language, :theme, :answers, :skill_scores, :has_results)
            ON CONFLICT(id) DO UPDATE SET
                user_name = excluded.user_name,
                avatar_path = excluded.avatar_path,
                language = excluded.language,
                theme = excluded.theme,
                answers = excluded.answers,
                skill_scores = excluded.skill_scores,
                has_results = excluded.has_results
            """,
            current,
        )
        conn.commit()
        conn.close()
    except Exception:
        # Persistence is a nice-to-have; never let a save failure crash the app.
        pass


def save_last_assessment(answers, skill_scores):
    """Convenience helper: store a finished assessment's raw answers and
    computed skill scores so results can be shown again on next launch."""
    # Save the answers and skill scores as JSON strings.
    save_profile(
        answers=json.dumps(answers, ensure_ascii=False),
        skill_scores=json.dumps(skill_scores, ensure_ascii=False),
        has_results=1,
    )


def get_saved_skill_scores(profile):
    """Parse the stored skill_scores JSON back into a dict, or None."""
    # Check if skill_scores exists in the profile.
    if not profile.get("skill_scores"):
        return None
    try:
        # Parse the JSON string into a Python dictionary.
        return json.loads(profile["skill_scores"])
    except Exception:
        # Return None if parsing fails.
        return None