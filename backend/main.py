from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os, json, io, uuid
from PIL import Image
import numpy as np
import cv2
import face_recognition

from database import Base, engine, SessionLocal
from models import KnownFace, UploadedPhoto
from schemas import KnownFaceOut, UploadedPhotoOut

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Face Recognition API",
    description="APIs for uploading known faces, checking faces, and retrieving statistics.",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc UI
    openapi_url="/openapi.json"
)

# Allow your frontend origin
origins = [
    "http://localhost:3000",  # Next.js frontend dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "images/uploads"
PROCESSED_FOLDER = "images/processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility: Extract encoding from known image
def extract_face_encoding(image_stream):
    image = face_recognition.load_image_file(image_stream)
    encodings = face_recognition.face_encodings(image)
    if encodings:
        return encodings[0].tolist()
    return None

# Utility: Compare faces and draw boxes using OpenCV
def compare_faces_and_draw_boxes(image_bytes, known_encodings):
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    names = []

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        for known_name, known_encoding in known_encodings:
            match = face_recognition.compare_faces([known_encoding], encoding, tolerance=0.5)
            if match[0]:
                name = known_name
                break

        names.append(name)

        # Draw rectangle & name using OpenCV
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    return pil_image, names

# 1. Upload known face
@app.post("/upload-known")
async def upload_known(name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    encoding = extract_face_encoding(io.BytesIO(contents))
    if encoding is None:
        raise HTTPException(status_code=400, detail="No face detected in the image")

    face = KnownFace(name=name, encoding=json.dumps(encoding))
    db.add(face)
    db.commit()
    db.refresh(face)

    return {"message": "Known face saved", "id": face.id, "name": face.name}

# 2. Get all known faces
@app.get("/known-faces", response_model=list[KnownFaceOut])
def get_known_faces(db: Session = Depends(get_db)):
    return db.query(KnownFace).all()

# 3. Upload photo and detect faces
@app.post("/upload-photo", response_model=UploadedPhotoOut)
async def upload_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    image_id = str(uuid.uuid4())
    original_path = os.path.join(UPLOAD_FOLDER, f"{image_id}_{file.filename}")

    with open(original_path, "wb") as f:
        f.write(contents)

    # Load known encodings
    known_faces = db.query(KnownFace).all()
    known_encodings = [(k.name, json.loads(k.encoding)) for k in known_faces]

    processed_image, names_detected = compare_faces_and_draw_boxes(contents, known_encodings)
    processed_path = os.path.join(PROCESSED_FOLDER, f"processed_{image_id}.jpg")
    processed_image.save(processed_path)

    photo = UploadedPhoto(
        filename=os.path.basename(original_path),
        processed_filename=os.path.basename(processed_path),
        detected_faces=json.dumps(names_detected)
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo

# 4. Get all uploaded photos (filterable)
@app.get("/photos", response_model=list[UploadedPhotoOut])
def get_photos(person: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(UploadedPhoto)
    if person:
        query = query.filter(UploadedPhoto.detected_faces.like(f"%{person}%"))
    return query.all()

# Optional: Serve processed image
@app.get("/processed/{filename}")
def get_processed_image(filename: str):
    path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="Image not found")

@app.get("/stats")
def get_stats():
    db = SessionLocal()
    try:
        known_faces = db.query(KnownFace).count()
        total_photos = db.query(UploadedPhoto).count()
        unknown_faces = db.query(UploadedPhoto).filter(UploadedPhoto.detected_faces.contains('"Unknown"')).count()
        return {
            "known_faces": known_faces,
            "total_photos": total_photos,
            "unknown_faces": unknown_faces
        }
    finally:
        db.close()