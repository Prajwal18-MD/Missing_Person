# Missing Person Detection System

A complete end-to-end web application for detecting missing persons using facial recognition.

## Features

- User registration and authentication
- Missing person case creation with face detection
- Public sighting uploads (images/videos)
- Automated face matching with configurable thresholds
- Email notifications for matches
- Admin dashboard for case management
- Location tracking and history

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL
- **Face Recognition**: face_recognition (dlib)
- **Video Processing**: OpenCV
- **Frontend**: React.js
- **Storage**: Local filesystem
- **Notifications**: SMTP email

## Quick Start

1. **Clone and setup backend**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Setup database**:
```bash
# Create .env file with your database URL
cp .env.example .env
# Edit .env with your settings
```

3. **Run backend**:
```bash
python main.py
```

4. **Setup frontend**:
```bash
cd frontend
npm install
npm start
```

5. **Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Docker Setup

```bash
docker-compose up --build
```

## API Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /cases/` - Create missing person case
- `POST /sightings/` - Upload sighting
- `GET /admin/cases` - Admin view all cases
- `GET /admin/matches` - View match history

## Configuration

Edit `.env` file:
- Database connection
- SMTP settings for email notifications
- Face matching threshold (0.6-0.8)
- JWT secret key

## Project Structure

See folder structure below for complete file organization.