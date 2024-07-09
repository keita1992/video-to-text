from fastapi import FastAPI, File, UploadFile

from libs.google_client import GoogleClient
from schemas.annotation import Annotation
from services.file_handler import FileHandler
from services.video_to_text import VideoToText

app = FastAPI(limits={"content_length": 500 * 1000 * 1000})  # 500MB


@app.post("/video-to-text", status_code=200, response_model=list[Annotation])
async def video_to_text(file: UploadFile = File(...)):
    google_client = GoogleClient()
    file_handler = FileHandler()
    service = VideoToText(google_client=google_client, file_handler=file_handler)
    return await service.convert(file)
