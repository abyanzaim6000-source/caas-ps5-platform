async function bookSession() {
    const userId = document.getElementById("userId").value;
    const minutes = document.getElementById("minutes").value;
    const statusDiv = document.getElementById("status");

    statusDiv.innerText = "Booking...";

    const response = await fetch("/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, minutes: parseInt(minutes) })
    });
    const data = await response.json();

    if (data.success) {
        statusDiv.innerText = `Booked! (TEST MODE - your OTP is: ${data.otp}) Ends at ${data.ends_at}`;
    } else {
        statusDiv.innerText = `Booking failed: ${data.reason}`;
    }
}

async function verifySession() {
    const userId = document.getElementById("userId").value;
    const token = document.getElementById("otpInput").value;
    const statusDiv = document.getElementById("status");

    statusDiv.innerText = "Verifying...";

    const response = await fetch("/verify-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, token: token })
    });
    const data = await response.json();

    if (data.valid) {
        statusDiv.innerText = "OTP verified! (Stream would start here once Sunshine is connected)";
    } else {
        statusDiv.innerText = `Verification failed: ${data.reason}`;
    }
}
