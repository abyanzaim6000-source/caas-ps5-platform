import threading
from fastapi import FastAPI
from pydantic import BaseModel

from database import init_db
from booking import try_book, release_console
from otp import generate_otp, verify_otp
from timer import cutoff_watcher
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from delivery import deliver_otp
from booking import get_user_history

app = FastAPI()

# --- Run once at startup: create the DB and start the background timer ---
@app.on_event("startup")
def startup_event():
    init_db()
    # Run the cutoff watcher in a background thread so it doesn't block the server
    watcher_thread = threading.Thread(target=cutoff_watcher, daemon=True)
    watcher_thread.start()
    print("[MAIN] Server started, database ready, cutoff watcher running.")


# --- Request body shapes ---
class BookingRequest(BaseModel):
    user_id: str
    minutes: int

class OtpVerifyRequest(BaseModel):
    user_id: str
    token: str


# --- Endpoints ---
@app.get("/")
def root():
    return {"message": "CaaS backend is running"}

@app.post("/book")
def book_console(req: BookingRequest):
    result = try_book(req.user_id, req.minutes)
    if result["success"]:
        otp = generate_otp(req.user_id)
        delivery_result = deliver_otp(req.user_id, otp)
        result["otp_delivery"] = delivery_result
        # NOTE: 'otp' itself is intentionally NOT included in the response anymore —
        # it now only exists inside the SMS/email sent to the user.
    return result

@app.post("/verify-otp")
def verify(req: OtpVerifyRequest):
    result = verify_otp(req.user_id, req.token)
    return result

@app.post("/release")
def release():
    release_console()
    return {"released": True}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/app")
def serve_frontend():
    return FileResponse("templates/index.html")

@app.get("/history/{user_id}")
def history(user_id: str):
    return {"user_id": user_id, "sessions": get_user_history(user_id)}