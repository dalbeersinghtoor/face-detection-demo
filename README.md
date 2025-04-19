
# **Face Detection System with Docker**

This project consists of a **Face Detection Backend** (FastAPI) and **Frontend** (Next.js) to upload, store, and detect faces in photos. The application runs in Docker for easy deployment and development.

### **Technologies Used**
- **Backend**: FastAPI, Python 3.12, dlib, face-recognition, SQLite
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Database**: SQLite (for local development)
- **Docker**: For containerized development and production

---

## **Project Setup**

### **1. Clone the repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/dalbeersinghtoor/face-detection-demo
cd face-detection-demo
```

---

### **2. Backend Setup (FastAPI)**

The backend is built with **FastAPI** and uses **SQLite** for storing known faces and uploaded images.

#### **Steps to run the Backend with Docker:**

1. **Navigate to the `backend/` directory**:
   ```bash
   cd backend
   ```

2. **Build and run the backend Docker container**:
   ```bash
   docker-compose up --build
   ```

3. **Backend will be available at**: `http://localhost:8000`

---

#### **Backend APIs**:

- **POST `/upload-known`**: Upload a known face (name and image file).
- **GET `/known-faces`**: Retrieve all known faces.
- **POST `/upload-photo`**: Upload a photo for face detection.
- **GET `/photos`**: Get a list of photos with face detection results.
- **GET `/stats`**: Get statistics about the number of known faces, photos uploaded, and photos with unknown faces.

---

### **3. Frontend Setup (Next.js)**

The frontend is built with **Next.js**, **TypeScript**, and **Tailwind CSS**. It provides a UI for interacting with the backend API.

#### **Steps to run the Frontend with Docker:**

1. **Navigate to the `frontend/` directory**:
   ```bash
   cd frontend
   ```

2. **Build and run the frontend Docker container**:
   ```bash
   docker-compose up --build
   ```

3. **Frontend will be available at**: `http://localhost:3000`

---

#### **Frontend Pages**:

- **Dashboard** (`/`): Displays statistics about known faces, uploaded photos, and unknown faces.
- **Upload Known Faces** (`/upload-known`): Form to upload new known faces.
- **Upload Photos** (`/upload-photos`): Upload photos for face detection.
- **View Photos** (`/view-photos`): View uploaded photos with face detection results and filter by known faces.

---

### **4. Docker Configuration**

The project uses **Docker Compose** to orchestrate both the frontend and backend services.

- **`docker-compose.yml`**:
    - The **frontend** service runs the Next.js app.
    - The **backend** service runs the FastAPI app.
    - Volumes are used to persist data and enable hot reloading during development.

#### **Run Both Frontend and Backend**:

1. **Start both frontend and backend** with the following command:
   ```bash
   docker-compose up --build
   ```

2. **Frontend** will be available at: `http://localhost:3000`
3. **Backend** will be available at: `http://localhost:8000`



