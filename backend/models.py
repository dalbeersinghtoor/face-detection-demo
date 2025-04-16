from sqlalchemy import Column, Integer, String, Text
from database import Base

class KnownFace(Base):
    __tablename__ = "known_faces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    encoding = Column(Text, nullable=False)  # JSON serialized encoding

class UploadedPhoto(Base):
    __tablename__ = "uploaded_photos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    processed_filename = Column(String(255), nullable=False)
    detected_faces = Column(Text, nullable=False)  # JSON list of detected face names