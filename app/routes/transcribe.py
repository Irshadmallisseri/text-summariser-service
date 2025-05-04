import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils.whisper_transcriber import transcribe_audio
from app.logging_config import logger

router = APIRouter()

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac"}

@router.post("/transcribe-audio")
async def transcribe(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"Rejected file '{file.filename}' — unsupported extension: {ext}")
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    logger.info(f"Received file '{file.filename}' for transcription")

    contents = await file.read()

    try:
        transcription = await transcribe_audio(contents, file.filename)
        logger.info(f"Transcription successful for '{file.filename}'")
    except Exception as e:
        logger.error(f"Transcription failed for '{file.filename}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Transcription failed")

    return {"transcription": transcription}
