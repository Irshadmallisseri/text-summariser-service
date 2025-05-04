from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from dotenv import load_dotenv
import os
from app.logging_config import logger

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "facebook/bart-large-cnn")
MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", "512"))
ABSOLUTE_MAX_SUMMARY_LENGTH = int(os.getenv("ABSOLUTE_MAX_SUMMARY_LENGTH", "300"))

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

logger.info(f"Loaded model '{MODEL_NAME}' on device '{device}'")

def summarize_text(text: str) -> str:
    logger.debug("Tokenizing input text")
    tokens = tokenizer(text, return_tensors="pt", truncation=True, max_length=MAX_INPUT_LENGTH)
    tokens = {key: val.to(device) for key, val in tokens.items()}
    input_length = tokens["input_ids"].shape[1]

    if input_length >= MAX_INPUT_LENGTH:
        logger.warning(f"Input too long ({input_length} >= {MAX_INPUT_LENGTH}), truncated.")

    min_length = max(80, int(input_length * 0.25))
    adjusted_max_length = max(min(ABSOLUTE_MAX_SUMMARY_LENGTH, int(input_length * 0.8)), min_length)

    logger.info(f"Generating summary (min={min_length}, max={adjusted_max_length})")

    summary_ids = model.generate(
        tokens["input_ids"],
        min_length=min_length,
        max_length=adjusted_max_length,
        no_repeat_ngram_size=3,
        num_beams=4,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    logger.debug("Summary generation complete")
    return summary