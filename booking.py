import sqlite3
from datetime import datetime, timedelta

def try_book(user_id: str, minutes: int) -> dict:
    conn = sqlite3.connect("caas.db")
    c = conn.cursor()
    c.execute("SELECT status FROM console_state WHERE id = 1")
    status = c.fetchone()[0]

    if status == "occupied":
        conn.close()
        return {"success": False, "reason": "Console currently in use"}

    now = datetime.utcnow()
    ends_at = now + timedelta(minutes=minutes)

    # Register user if new, otherwise this just does nothing (INSERT OR IGNORE)
    c.execute("INSERT OR IGNORE INTO users (contact) VALUES (?)", (user_id,))

    c.execute("""
        UPDATE console_state
        SET status = 'occupied', current_user_id = ?, session_ends_at = ?
        WHERE id = 1
    """, (user_id, ends_at))

    # Log this session in history (ended_at filled in later, on release)
    c.execute("""
        INSERT INTO session_history (user_contact, started_at, ended_at, minutes_booked)
        VALUES (?, ?, NULL, ?)
    """, (user_id, now, minutes))

    c.execute("UPDATE users SET total_sessions = total_sessions + 1 WHERE contact = ?", (user_id,))

    conn.commit()
    conn.close()
    return {"success": True, "ends_at": ends_at.isoformat()}


def release_console():
    conn = sqlite3.connect("caas.db")
    c = conn.cursor()

    # Find who's currently occupying, so we can close out their history row
    c.execute("SELECT current_user_id FROM console_state WHERE id = 1")
    current_user = c.fetchone()[0]

    if current_user:
        c.execute("""
            UPDATE session_history
            SET ended_at = ?
            WHERE user_contact = ? AND ended_at IS NULL
        """, (datetime.utcnow(), current_user))

    c.execute("""
        UPDATE console_state
        SET status = 'free', current_user_id = NULL, session_ends_at = NULL
        WHERE id = 1
    """)
    conn.commit()
    conn.close()


def get_user_history(user_id: str) -> list:
    conn = sqlite3.connect("caas.db")
    c = conn.cursor()
    c.execute("""
        SELECT started_at, ended_at, minutes_booked
        FROM session_history
        WHERE user_contact = ?
        ORDER BY started_at DESC
    """, (user_id,))
    rows = c.fetchall()
    conn.close()
    return [
        {"started_at": r[0], "ended_at": r[1], "minutes_booked": r[2]}
        for r in rows
    ]


if __name__ == "__main__":
    print("User A books 30 mins:", try_book("user_A", 30))
    print("User B tries to book while occupied:", try_book("user_B", 15))
    release_console()
    print("Console released.")
    print("User A's history:", get_user_history("user_A"))