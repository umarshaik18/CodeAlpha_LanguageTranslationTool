from io import BytesIO

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from gtts import gTTS

from backend.models.translation import (
    TranslationRequest,
    TranslationResponse,
)
from backend.services.translator import (
    Translator,
    TranslationError,
)


app = FastAPI(
    title="Language Translation Tool API",
    description="Free multilingual translation API",
    version="1.0.0",
)


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


translator = Translator()


SUPPORTED_LANGUAGES = {
    "en": "English",
    "te": "Telugu",
    "hi": "Hindi",
    "ta": "Tamil",
    "es": "Spanish",
}


TTS_LANGUAGES = {
    "en": "en",
    "te": "te",
    "hi": "hi",
    "ta": "ta",
    "es": "es",
}


@app.get("/")
async def root():
    return {
        "message": "Language Translation Tool API is running",
        "status": "ok",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "translation",
    }


@app.get("/languages")
async def get_languages():
    return SUPPORTED_LANGUAGES


@app.post(
    "/translate",
    response_model=TranslationResponse,
)
async def translate_text(
    request: TranslationRequest,
):
    source = request.source_language.lower().strip()
    target = request.target_language.lower().strip()
    text = request.text.strip()

    if source not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported source language: {source}",
        )

    if target not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported target language: {target}",
        )

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    try:
        translated = await translator.translate(
            text=text,
            source_language=source,
            target_language=target,
        )

        return TranslationResponse(
            translated_text=translated,
            source_language=source,
            target_language=target,
        )

    except TranslationError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )


@app.post("/tts")
async def text_to_speech(
    text: str,
    language: str,
):
    """
    Convert translated text into speech.
    Returns an MP3 audio response.
    """

    text = text.strip()
    language = language.lower().strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    if language not in TTS_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported TTS language: {language}",
        )

    try:
        audio_buffer = BytesIO()

        speech = gTTS(
            text=text,
            lang=TTS_LANGUAGES[language],
            slow=False,
        )

        speech.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline",
                "Cache-Control": "no-cache",
            },
        )

    except Exception as error:
        print(f"TTS error: {error}")

        raise HTTPException(
            status_code=502,
            detail="Unable to generate speech.",
        )