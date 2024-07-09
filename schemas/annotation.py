from pydantic import BaseModel


class Annotation(BaseModel):
    start_time: int
    end_time: int
    text: str
