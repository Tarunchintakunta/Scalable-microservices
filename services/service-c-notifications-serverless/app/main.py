"""
Main FastAPI application for Service C - Notifications
Wraps the lambda_like handler for local development
"""
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict

from app.lambda_like import handle_event

app = FastAPI(
    title="Service C - Notifications",
    description="Serverless-style notification service",
    version="1.0.0"
)


class NotificationEvent(BaseModel):
    type: str
    data: Dict


@app.post("/notify")
async def notify(event: NotificationEvent):
    """
    Notification endpoint
    Calls the lambda-like handler
    """
    result = handle_event(event.model_dump())
    return result


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "Notifications",
        "version": "1.0.0",
        "status": "running",
        "note": "Lambda-ready notification service"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
