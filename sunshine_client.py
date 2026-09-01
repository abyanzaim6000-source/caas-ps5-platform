"""
Stub client for Sunshine streaming server integration.

Once real hardware is available, the functions below will be updated to
make actual HTTP calls to the Sunshine API running on the host PC
(reached via the WireGuard/Tailscale tunnel discussed in Phase 2).

For now, every function just simulates success so the rest of the app
can be built and tested without hardware.
"""

def whitelist_user(user_id: str, session_token: str) -> dict:
    """
    In the real version: calls Sunshine's pairing/auth API to allow
    this specific user's connection through for the duration of their
    session.
    """
    print(f"[SUNSHINE-STUB] Whitelisting {user_id} with token {session_token}")
    return {"whitelisted": True}


def get_stream_url(user_id: str) -> str:
    """
    In the real version: returns the actual relay/WebRTC URL the
    frontend's Moonlight-WebAssembly client should connect to.
    """
    print(f"[SUNSHINE-STUB] Generating stream URL for {user_id}")
    return f"wss://stub.local/relay/{user_id}"


def kick_user_and_rest_console(user_id: str) -> dict:
    """
    In the real version: forcibly terminates the user's stream session
    and sends a rest-mode command to the PS5.
    This is called by timer.py when a session's paid time expires.
    """
    print(f"[SUNSHINE-STUB] Kicking {user_id} and putting console to rest")
    return {"kicked": True, "console_rested": True}


if __name__ == "__main__":
    whitelist_user("test_user", "abc123")
    print(get_stream_url("test_user"))
    kick_user_and_rest_console("test_user")