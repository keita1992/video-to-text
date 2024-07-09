from fastapi import HTTPException, UploadFile

from libs.google_client import GoogleClient
from schemas.annotation import Annotation

from .file_handler import FileHandler


class VideoToText:
    def __init__(self, google_client: GoogleClient, file_handler: FileHandler):
        self.google_client = google_client
        self.file_handler = file_handler

    async def convert(self, file: UploadFile) -> list[Annotation]:
        is_video, mime_type = await self.file_handler.is_video(file)
        if not is_video:
            raise HTTPException(
                status_code=400,
                detail=f"The file is not a video. Detected MIME type: {mime_type}",
            )

        tmp_filepath = await self.file_handler.save_temp_file(file)

        with open(tmp_filepath, "rb") as video_file:
            video_content = video_file.read()

        return self.google_client.video_to_text(video_content)
