import whisper
import tempfile
import os
from pathlib import Path
import asyncio
import time
from app.logging_config import logger

ffmpeg_dir = Path(__file__).resolve().parents[2] / "ffmpeg"
os.environ["PATH"] = str(ffmpeg_dir) + os.pathsep + os.environ["PATH"]

model = whisper.load_model("base", device="cuda")
logger.info("Whisper model loaded on CUDA")

def _sync_transcribe(data: bytes, filename: str) -> str:
    suffix = os.path.splitext(filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    logger.info(f"Transcription started for '{filename}'")
    start_time = time.time()

    try:
        result = model.transcribe(tmp_path)
        duration = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Transcription completed for '{filename}' in {duration}ms")
        return result["text"]
    except Exception as e:
        logger.error(f"Transcription failed for '{filename}': {str(e)}", exc_info=True)
        raise
    finally:
        os.remove(tmp_path)
        logger.debug(f"Temporary file deleted: {tmp_path}")

async def transcribe_audio(data: bytes, filename: str) -> str:
    return await asyncio.to_thread(_sync_transcribe, data, filename)
