from pydantic import BaseModel

class AudioUploadResponse(BaseModel):
    filename: str
    content_type: str
    size: int