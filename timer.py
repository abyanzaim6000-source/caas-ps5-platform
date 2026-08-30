import sqlite3
import time
from datetime import datetime
from booking import release_console

def check_and_cutoff():
    """Checks if the current session has expired, and if so, ends it."""
    conn = sqlite3.connect("caas.db")
    c = conn.cursor()
    c.execute("SELECT status, current_user_id, session_ends_at FROM console_state WHERE id = 1")
    status, user_id, ends_at = c.fetchone()
    conn.close()

    if status == "occupied" and ends_at:
        if datetime.utcnow() >= datetime.fromisoformat(ends_at):
            print(f"[TIMER] Session for {user_id} has expired. Cutting off now.")
            # In the real system, this is where we'd also call Sunshine
            # to kill the stream and rest the console — we'll add that
            # once we build sunshine_client.py
            release_console()
            return True
    return False


def cutoff_watcher(poll_seconds: int = 5):
    """Runs forever, checking every few seconds for expired sessions."""
    print("[TIMER] Cutoff watcher started.")
    while True:
        check_and_cutoff()
        time.sleep(poll_seconds)


if __name__ == "__main__":
    # Quick manual test: book a session for a few seconds, then watch
    # the timer catch and release it automatically.
    from booking import try_book

    print(try_book("user_A", minutes=0))  # 0-minute booking, expires almost instantly
    print("Waiting for the timer to catch the expired session...")

    for _ in range(5):
        expired = check_and_cutoff()
        if expired:
            print("Session was cut off successfully.")
            break
        time.sleep(2)