# Online Quiz Cheating Detector

A real-time quiz monitoring application built with FastAPI, React, PostgreSQL, SQLAlchemy Core, Alembic, and WebSockets.

The application receives simulated quiz-answer submissions, analyzes them for suspicious behavior, stores submissions and cheating flags in PostgreSQL, calculates a risk score, and displays activity live on a React dashboard.

## Features

- Live quiz submission monitoring
- FastAPI REST API
- WebSocket real-time updates
- PostgreSQL database
- SQLAlchemy Core database access
- Alembic database migrations
- React frontend built with Vite
- Recent submission history
- Responsive dashboard
- Risk score from 0–100

## Cheating Detection Rules

The system checks each submission for:

1. **Too-fast answer**
   - Flags answers submitted in under 2 seconds.

2. **Faster than usual**
   - Compares the current answer time with the student's recent rolling average.
   - Flags answers completed in less than half of that average.

3. **Same wrong answer**
   - Flags when two different students submit the same wrong answer to the same question within 5 seconds.

Each rule contributes to an overall risk score, capped at 100.

## Architecture

```text
React Frontend
      |
      | REST API + WebSocket
      v
FastAPI Backend
      |
      | SQLAlchemy Core
      v
PostgreSQL