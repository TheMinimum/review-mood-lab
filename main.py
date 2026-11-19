from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from model import MODEL_VERSION, analyze_sentiment

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Review Mood Lab", version=MODEL_VERSION)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class ReviewRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

    @field_validator("text")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("review must not be blank")
        return value


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "review-mood-lab", "model_version": MODEL_VERSION}


@app.post("/analyze")
def analyze(review: ReviewRequest):
    return analyze_sentiment(review.text.strip())
