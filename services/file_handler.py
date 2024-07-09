import shutil
import tempfile
from typing import Tuple

import magic
from fastapi import UploadFile


class FileHandler:
    @staticmethod
    async def save_temp_file(file: UploadFile) -> str:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            return temp_file.name

    @staticmethod
    async def is_video(file: UploadFile) -> Tuple[bool, str]:
        mime_type = magic.from_buffer(await file.read(1024), mime=True)
        await file.seek(0)
        return mime_type.startswith("video"), mime_type
