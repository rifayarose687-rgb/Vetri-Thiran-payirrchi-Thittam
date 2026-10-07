from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import settings

app = FastAPI(title=settings.app_name, version="1.0.0")


class RecommendationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    context: str | None = Field(default=None, max_length=4000)


def _build_mock_recommendation(prompt: str, context: str | None) -> str:
    prompt_text = prompt.strip()
    context_text = f" Context: {context.strip()}" if context and context.strip() else ""
    return (
        f"PocketSmart AI suggests a concise, actionable plan for: '{prompt_text}'."
        f"{context_text} Keep the approach practical, measurable, and easy to execute."
    )


async def _generate_recommendation(prompt: str, context: str | None) -> str:
    if settings.mock_recommendations or not settings.gemini_enabled or not settings.gemini_api_key:
        return _build_mock_recommendation(prompt, context)

    try:
        from google import genai
    except ImportError:
        return _build_mock_recommendation(prompt, context)

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        combined_prompt = prompt.strip()
        if context and context.strip():
            combined_prompt = f"{combined_prompt}\n\nAdditional context:\n{context.strip()}"
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=combined_prompt,
        )
        generated_text = getattr(response, "text", None)
        if generated_text:
            return generated_text.strip()
    except Exception:
        return _build_mock_recommendation(prompt, context)

    return _build_mock_recommendation(prompt, context)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
@app.get("/api/v1/health")
async def healthcheck() -> dict[str, Any]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
    }


@app.get("/api/v1/config")
async def app_config() -> dict[str, Any]:
    return {
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "gemini_enabled": settings.gemini_enabled,
        "mock_recommendations": settings.mock_recommendations,
        "max_upload_mb": settings.max_upload_mb,
    }


@app.post("/api/v1/recommendations")
async def create_recommendations(payload: RecommendationRequest) -> dict[str, Any]:
    recommendation = await _generate_recommendation(payload.prompt, payload.context)
    return {
        "prompt": payload.prompt,
        "context": payload.context,
        "recommendation": recommendation,
    }


@app.get("/api/v1/status")
async def status() -> dict[str, Any]:
    return {
        "status": "ready",
        "app": settings.app_name,
        "environment": settings.app_env,
    }
