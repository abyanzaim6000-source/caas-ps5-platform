# CaaS — Console-as-a-Service

A web platform that lets users rent timed, remote access to a physical PS5 console and play it directly through their browser. Built from scratch as a learning project covering backend API design, booking/concurrency logic, OTP-based authentication, and remote game streaming.

## How it works

1. A user visits the site and checks if the console is available.
2. They book a time slot, triggering a one-time passcode (OTP) sent via SMS or email.
3. Entering the correct OTP verifies their session.
4. The platform streams the console's video feed into the browser via [Sunshine](https://github.com/LizardByte/Sunshine) and Moonlight.
5. A background timer automatically ends the session and frees the console the moment the paid time runs out.

## Tech stack

- **Backend**: Python, FastAPI
- **Database**: SQLite
- **OTP delivery**: MSG91 (SMS), Resend (email)
- **Streaming**: Sunshine + Moonlight-WebAssembly (in progress — currently stubbed pending hardware setup)
- **Frontend**: HTML/CSS/vanilla JS
- **Deployment**: Render

## Features

- Single-console booking lock — only one user can be active at a time, others are blocked until release
- OTP generation with expiry and single-use verification
- Automated cutoff timer that force-ends expired sessions
- Per-user session history tracking
- Stubbed Sunshine integration layer, ready to swap in real hardware calls

## Project structure

caas-project/
├── main.py # FastAPI app and routes
├── database.py # SQLite schema and init
├── booking.py # Booking logic, concurrency lock, session history
├── otp.py # OTP generation, verification, expiry
├── delivery.py # SMS/email OTP delivery (MSG91, Resend)
├── timer.py # Background cutoff watcher
├── sunshine_client.py # Streaming integration (currently stubbed)
├── templates/index.html # Frontend page
└── static/app.js # Frontend logic


## Status

Core booking, OTP, and user-history system is fully built and deployed. Streaming integration is stubbed pending physical hardware access to the console.

## Why this project

Built to learn full-stack development end-to-end — backend architecture, auth flows, deployment, and the real-world debugging that comes with all of it — while solving an actual problem: console access shared safely among multiple remote users.
EOF
