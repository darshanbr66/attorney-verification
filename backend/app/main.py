# main.py

import asyncio
import sys

# Windows Playwright Fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="AI Attorney Verification System",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router)


@app.get("/")
def root():

    return {
        "status": "success",
        "message": "AI Attorney Verification System API Running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }