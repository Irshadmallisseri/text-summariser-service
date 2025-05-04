from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import summarize, transcribe
from app.middleware.request_logger import RequestLoggingMiddleware

app = FastAPI()

app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(summarize.router, prefix="/api", tags=["Summarization"])
app.include_router(transcribe.router, prefix="/api", tags=["Transcription"])

@app.get("/")
def health_check():
    return {"message": "API is running"}
