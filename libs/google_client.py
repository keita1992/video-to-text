import os

from dotenv import load_dotenv
from google.cloud import videointelligence
from google.oauth2 import service_account

from schemas.annotation import Annotation


class GoogleClient:
    def __init__(self):
        load_dotenv()
        key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not key_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set"
            )
        credentials = service_account.Credentials.from_service_account_file(key_path)
        self.video_client = videointelligence.VideoIntelligenceServiceClient(
            credentials=credentials
        )

    def video_to_text(self, video_content: bytes) -> list[Annotation]:
        features = [videointelligence.Feature.TEXT_DETECTION]

        operation = self.video_client.annotate_video(
            request={
                "features": features,
                "input_content": video_content,
            }
        )
        result = operation.result(timeout=180)
        annotation_results = result.annotation_results[0]

        all_texts = []
        for text_annotation in annotation_results.text_annotations:
            if text_annotation.segments:
                for segment in text_annotation.segments:
                    start_time = segment.segment.start_time_offset
                    end_time = segment.segment.end_time_offset
                    all_texts.append(
                        (start_time.seconds, end_time.seconds, text_annotation.text)
                    )

        all_texts.sort(key=lambda x: x[0])

        return [
            Annotation(start_time=start_time, end_time=end_time, text=text)
            for start_time, end_time, text in all_texts
        ]
