import os
import resend
import requests
from dotenv import load_dotenv

load_dotenv()

MSG91_AUTH_KEY = os.getenv("MSG91_AUTH_KEY")
resend.api_key = os.getenv("RESEND_API_KEY")

def is_email(user_id: str) -> bool:
    return "@" in user_id

def send_sms_otp(phone: str, otp: str):
    """Sends OTP via MSG91. Assumes 10-digit Indian phone number."""
    url = "https://control.msg91.com/api/v5/otp"
    params = {
        "authkey": MSG91_AUTH_KEY,
        "mobile": f"91{phone}",
        "otp": otp,
        "sender": "CAASGO",
    }
    response = requests.post(url, params=params, timeout=10)
    return response.status_code == 200

def send_email_otp(email: str, otp: str):
    """Sends OTP via Resend."""
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",  # Resend's default test sender — works immediately, no domain setup needed
            "to": email,
            "subject": "Your CaaS OTP",
            "text": f"Your OTP is: {otp}",
        })
        return True
    except Exception as e:
        print(f"[DELIVERY] Resend error: {e}")
        return False

def deliver_otp(user_id: str, otp: str) -> dict:
    if is_email(user_id):
        success = send_email_otp(user_id, otp)
        method = "email"
    else:
        success = send_sms_otp(user_id, otp)
        method = "sms"
    return {"delivered": success, "method": method}


if __name__ == "__main__":
    result = deliver_otp("abyanzaim6000@gmail.com", "123456")
    print(result)