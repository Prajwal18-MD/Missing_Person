# 🚀 START HERE - Missing Person Detection System

## 📋 Quick Overview
This is a complete AI-powered Missing Person Detection System that uses facial recognition to help find missing people. Anyone can upload sightings, and the system automatically matches faces with missing person cases.

## 🎯 What This System Does
- **Create Missing Person Cases**: Upload photos of missing people
- **Report Sightings**: Anyone can upload photos/videos of people they've seen
- **AI Face Matching**: Automatically compares faces and finds matches
- **Instant Alerts**: Sends email notifications when matches are found
- **Location Tracking**: Maps where sightings occurred
- **Admin Dashboard**: Manage cases and verify matches

---

## 🛠️ SETUP INSTRUCTIONS

### Option 1: Quick Start with Docker (Recommended)
```bash
# 1. Clone/Download the project
cd "Missing Person"

# 2. Start everything with one command
docker-compose up --build

# 3. Wait for services to start (2-3 minutes)
# You'll see "Application startup complete" when ready
```

### Option 2: Manual Setup

#### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

#### Backend Setup
```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment (recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
copy .env.example .env
# Edit .env file with your settings (see Configuration section)

# 5. Start backend
python main.py
```

#### Frontend Setup
```bash
# 1. Navigate to frontend (new terminal)
cd frontend

# 2. Install dependencies
npm install

# 3. Start frontend
npm start
```

---

## ⚙️ CONFIGURATION

### Required Settings (Edit `backend/.env`)
```env
# Database (SQLite for demo, PostgreSQL for production)
DATABASE_URL=sqlite:///./missing_persons.db

# JWT Security
SECRET_KEY=your-super-secret-key-change-this

# Email Settings (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Face Recognition
FACE_MATCH_THRESHOLD=0.6
```

### Gmail Setup for Notifications
1. Enable 2-Factor Authentication
2. Generate App Password: Google Account → Security → App passwords
3. Use App Password in SMTP_PASSWORD

---

## 🌐 ACCESS THE APPLICATION

After setup, access these URLs:

| Service | URL | Description |
|---------|-----|-------------|
| **Main App** | http://localhost:3000 | React frontend |
| **API** | http://localhost:8000 | FastAPI backend |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |

---

## 📱 HOW TO USE THE SYSTEM

### 🏠 First Page (Home Page)
When you open http://localhost:3000, you'll see:

```
┌─────────────────────────────────────────────────────────┐
│  Missing Person Detection System                        │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Report Sighting │  │ Create Case     │              │
│  │  (Public)        │  │ (Login Required)│              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  How It Works:                                          │
│  1. Upload Missing Person Photo                         │
│  2. Community Reports Sightings                         │
│  3. AI Matches Faces                                    │
│  4. Instant Alerts                                      │
└─────────────────────────────────────────────────────────┘
```

### 👤 User Registration
1. Click "Register" in top navigation
2. Fill form:
   - Email: your-email@example.com
   - Phone: +1234567890
   - Password: minimum 6 characters
3. Click "Register" → Success message → Redirects to login

### 🔐 Login Process
1. Click "Login" in navigation
2. Enter email and password
3. Success → Redirects to home with new navigation options

### 📝 Creating a Missing Person Case
**Requirements**: Must be logged in

1. Click "Create Case" in navigation
2. Fill the form:
   ```
   Name: John Doe
   Address: 123 Main Street, City (optional)
   Aadhaar: 1234-5678-9012 (optional, will be encrypted)
   Email: contact@family.com (for alerts)
   Phone: +1234567890
   Photo: Upload clear face photo (REQUIRED)
   ```
3. Click "Create Case"
4. System processes photo and extracts face
5. Success → Case created, face matching activated

### 📸 Reporting a Sighting (Public - No Login Required)
1. Click "Report Sighting" 
2. Upload photo or video (Max 10MB)
3. Add location:
   - Click "Use Current Location" (GPS)
   - OR manually enter coordinates
   - OR enter location name
4. Click "Upload Sighting"
5. System processes in background and checks for matches

### 📊 My Cases Dashboard
**Requirements**: Must be logged in

1. Click "My Cases"
2. View all your created cases
3. See case status: Active/Found
4. Delete cases if needed

### 👨‍💼 Admin Dashboard
**Requirements**: Admin account

1. Click "Admin Dashboard"
2. Tabs available:
   - **Overview**: Statistics and metrics
   - **Cases**: All missing person cases
   - **Matches**: Face recognition results
   - **Locations**: Map view of sightings

---

## 📧 EMAIL NOTIFICATIONS

### When You'll Receive Emails:
1. **Case Created**: Confirmation email
2. **Match Found**: Alert with:
   - Matched person's name
   - Confidence score (e.g., 87%)
   - Location of sighting
   - Timestamp
   - Matched face image (attached)
3. **Person Found**: When admin marks case as resolved

### Sample Match Alert Email:
```
Subject: ALERT: Possible sighting of John Doe

MISSING PERSON ALERT

A possible match has been found for: John Doe

Details:
- Confidence Score: 87.3%
- Location: Central Park, New York
- Time: 2024-01-15 14:30:25

Please verify this match as soon as possible.
```

---

## 🗺️ Location Features

### GPS Integration:
- **Automatic**: Click "Use Current Location" button
- **Manual**: Enter latitude/longitude coordinates
- **Named**: Enter location description (e.g., "Central Mall")

### Map Visualization:
- Interactive map shows all sighting locations
- Click markers to see details
- Timeline view of person's movement

---

## 📁 File Upload Guidelines

### Supported Formats:
- **Images**: JPEG, PNG, JPG
- **Videos**: MP4, AVI, MOV
- **Max Size**: 10MB per file

### Photo Requirements:
- Clear, recent photo
- Face clearly visible
- Good lighting
- Minimum face size: 50x50 pixels

### Video Processing:
- System samples 1 frame per second
- Extracts all faces from each frame
- Processes each face separately

---

## 🔧 TROUBLESHOOTING

### Common Issues:

#### "No face detected" error:
- Use clearer photo with visible face
- Ensure good lighting
- Face should be at least 50x50 pixels

#### Email notifications not working:
- Check SMTP settings in .env file
- Verify Gmail app password
- Check spam folder

#### Docker issues:
```bash
# Stop and restart
docker-compose down
docker-compose up --build

# Check logs
docker-compose logs backend
docker-compose logs frontend
```

#### Port conflicts:
- Backend (8000): Change in docker-compose.yml
- Frontend (3000): Change in docker-compose.yml
- Database (5432): Change PostgreSQL port

---

## 🎮 TESTING THE SYSTEM

### Quick Test Workflow:
1. **Register** a new account
2. **Create** a missing person case with a clear photo
3. **Upload** a sighting with the same person's photo
4. **Wait** 30-60 seconds for processing
5. **Check** email for match notification
6. **Login as admin** to verify match

### Sample Test Data:
- Use different photos of the same person
- Test with family photos
- Try group photos (system detects multiple faces)

---

## 📞 SUPPORT

### Log Files:
- Backend logs: Console output or docker logs
- Frontend logs: Browser developer console
- Database: Check connection in backend logs

### Performance:
- Face processing: 5-30 seconds per image
- Video processing: 1-5 minutes depending on length
- Email delivery: 10-30 seconds

### Scaling:
- SQLite: Good for testing (100+ cases)
- PostgreSQL: Production use (1000+ cases)
- File storage: Local (can extend to cloud storage)

---

## 🚀 NEXT STEPS

1. **Test the system** with sample photos
2. **Configure email** settings for notifications
3. **Create admin account** for management
4. **Deploy to production** using Docker
5. **Scale database** to PostgreSQL for larger usage

**Ready to help find missing persons! 🙏**