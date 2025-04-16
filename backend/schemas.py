from pydantic import BaseModel
from typing import List

class KnownFaceOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UploadedPhotoOut(BaseModel):
    id: int
    filename: str
    processed_filename: str
    detected_faces: str  # JSON string of list of names

    class Config:
        orm_mode = True
