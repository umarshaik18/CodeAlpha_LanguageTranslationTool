from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    source_language: str
    target_language: str


class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str