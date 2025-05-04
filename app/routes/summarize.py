from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.summarizer import summarize_text
from app.logging_config import logger

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/summarize-text")
async def summarize(input: TextInput):
    text = input.text.strip()

    if not text:
        logger.warning("Summarization failed: empty input text")
        raise HTTPException(status_code=400, detail="Empty input text")
    
    logger.info("Summarization request received")
    summary = summarize_text(text)
    logger.info("Summarization completed successfully")
    
    return {"summary": summary}