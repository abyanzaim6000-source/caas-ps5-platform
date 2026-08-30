import secrets
from datetime import datetime, timedelta

# In-memory store for now — fine for testing.
# Later, when we deploy, we'll swap this for Redis so it survives server restarts.
_active_tokens = {}  # user_id -> {"token": str, "expires_at": datetime}

OTP_VALIDITY_MINUTES = 5  # user has 5 minutes to enter it

def generate_otp(user_id: str) -> str:
    token = secrets.token_hex(4)  # 8-character random token, e.g. "a3f9c210"
    expires_at = datetime.utcnow() + timedelta(minutes=OTP_VALIDITY_MINUTES)
    _active_tokens[user_id] = {"token": token, "expires_at": expires_at}
    return token

def verify_otp(user_id: str, submitted_token: str) -> dict:
    record = _active_tokens.get(user_id)
    if record is None:
        return {"valid": False, "reason": "No OTP was generated for this user"}

    if datetime.utcnow() > record["expires_at"]:
        _active_tokens.pop(user_id, None)  # expired, clean it up
        return {"valid": False, "reason": "OTP expired, please request a new one"}

    if not secrets.compare_digest(record["token"], submitted_token):
        return {"valid": False, "reason": "Incorrect OTP"}

    _active_tokens.pop(user_id, None)  # single-use — clear it once verified
    return {"valid": True, "reason": "OK"}

def clear_otp(user_id: str):
    _active_tokens.pop(user_id, None)


if __name__ == "__main__":
    token = generate_otp("user_A")
    print("Generated token for user_A:", token)

    print("Verify with correct token:", verify_otp("user_A", token))
    # Note: token is now cleared since it was single-use above.
    # Generate a fresh one to test the wrong-token and expiry cases separately:

    token2 = generate_otp("user_B")
    print("Verify with wrong token:", verify_otp("user_B", "wrongtoken"))

    # Simulate expiry by manually backdating the expiry time
    _active_tokens["user_B"] = {"token": token2, "expires_at": datetime.utcnow() - timedelta(seconds=1)}
    print("Verify after manual expiry:", verify_otp("user_B", token2))