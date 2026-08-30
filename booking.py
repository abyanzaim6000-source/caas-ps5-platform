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

    ends_at = datetime.utcnow() + timedelta(minutes=minutes)
    c.execute("""
        UPDATE console_state
        SET status = 'occupied', current_user_id = ?, session_ends_at = ?
        WHERE id = 1
    """, (user_id, ends_at))
    conn.commit()
    conn.close()
    return {"success": True, "ends_at": ends_at.isoformat()}


def release_console():
    conn = sqlite3.connect("caas.db")
    c = conn.cursor()
    c.execute("""
        UPDATE console_state
        SET status = 'free', current_user_id = NULL, session_ends_at = NULL
        WHERE id = 1
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Quick manual test — simulates two users trying to book back to back
    print("User A books 30 mins:", try_book("user_A", 30))
    print("User B tries to book while occupied:", try_book("user_B", 15))
    release_console()
    print("Console released.")
    print("User B books after release:", try_book("user_B", 15))
    release_console()