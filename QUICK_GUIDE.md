# 📚 QUICK GUIDE - Missing Person Detection System

## 🚀 **INSTANT SETUP (30 SECONDS)**

### Step 1: Run Setup
```bash
# Just double-click this file:
setup.bat

# Or run from command line:
cd "Missing Person"
setup.bat
```

### Step 2: Wait for Magic ✨
- Backend installs automatically
- Frontend installs automatically  
- Both servers start automatically
- Browser opens automatically to http://localhost:3000

**That's it! The system is running!** 🎉

---

## ⚙️ **CONFIGURATION FILES**

### 📝 **Backend Configuration (`backend\.env`)**

**Location**: `backend\.env`  
**Auto-created**: Yes (with defaults)  
**Must Edit**: Email settings for notifications

```env
# Database (SQLite for demo, PostgreSQL for production)
DATABASE_URL=sqlite:///./missing_persons.db

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=missing-person-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 📧 EMAIL SETTINGS (REQUIRED FOR NOTIFICATIONS)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com        # ← CHANGE THIS
SMTP_PASSWORD=your-app-password           # ← CHANGE THIS  
FROM_EMAIL=your-email@gmail.com           # ← CHANGE THIS

# Face Recognition Settings
FACE_MATCH_THRESHOLD=0.6                  # 0.6 = 60% similarity required
MIN_FACE_SIZE=50                          # Minimum face size in pixels
MAX_FILE_SIZE=10485760                    # 10MB max upload

# File Storage
UPLOAD_DIR=uploads
```

### 🔧 **How to Setup Gmail for Notifications**

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account → Security → App passwords
   - Select "Mail" and generate password
   - Copy the 16-character password
3. **Update .env file**:
   ```env
   SMTP_USERNAME=youremail@gmail.com
   SMTP_PASSWORD=abcd efgh ijkl mnop    # The app password
   FROM_EMAIL=youremail@gmail.com
   ```

### 📱 **Frontend Configuration (Optional)**

**Location**: `frontend\src\services\api.js`  
**Default**: Works with backend on localhost:8000  
**Change if needed**: Different backend URL

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

---

## 🌐 **ACCESS POINTS**

| Service | URL | Purpose |
|---------|-----|---------|
| **Main App** | http://localhost:3000 | React frontend (users interact here) |
| **Backend API** | http://localhost:8000 | FastAPI server (handles AI processing) |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs (for developers) |
| **Database** | `backend/missing_persons.db` | SQLite file (stores all data) |
| **Uploads** | `backend/uploads/` | Stored photos and videos |

---

## 👤 **USER WORKFLOW & FEATURES**

### 🏠 **1. Home Page (First Visit)**
**URL**: http://localhost:3000

```
┌─────────────────────────────────────────────────────────┐
│  🔍 Missing Person Detection System                     │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  📸 Report      │  │  👤 Create      │              │
│  │  Sighting       │  │  Case           │              │
│  │  (Anyone)       │  │  (Login Req)    │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  How It Works:                                          │
│  1️⃣ Upload Missing Person Photo                        │
│  2️⃣ Community Reports Sightings                        │
│  3️⃣ AI Matches Faces Automatically                     │
│  4️⃣ Instant Email Alerts Sent                          │
└─────────────────────────────────────────────────────────┘
```

### 📝 **2. User Registration**
**Click**: "Register" in top navigation

**Form Fields**:
```
Email: user@example.com          (Required - for login & alerts)
Phone: +1234567890              (Required - contact info)
Password: ********              (Required - min 6 characters)
Confirm Password: ********      (Required - must match)
```

**Process**:
1. Fill form → Click "Register"
2. Success message appears
3. Auto-redirect to login page
4. Login with new credentials

### 🔐 **3. Login Process**
**Click**: "Login" in navigation

**Credentials**:
```
Email: your-registered-email@example.com
Password: your-password
```

**After Login - New Navigation**:
- ✅ Create Case
- ✅ My Cases  
- ✅ Admin Dashboard (if admin)
- ✅ Logout option

### 👤 **4. Creating Missing Person Case**
**Requirements**: Must be logged in  
**Click**: "Create Case"

**Form Fields**:
```
📝 Personal Information:
Name: John Doe                   (Required)
Address: 123 Main St, City      (Optional)
Aadhaar: 1234-5678-9012        (Optional - stored encrypted)
Email: family@contact.com        (Optional - for alerts)
Phone: +1234567890              (Optional)

📸 Photo Upload:
Photo: [Choose File]             (Required - clear face photo)
```

**Photo Requirements**:
- ✅ Clear, recent photo
- ✅ Face clearly visible
- ✅ Good lighting
- ✅ Supported: JPEG, PNG, JPG
- ✅ Max size: 10MB
- ✅ Minimum face size: 50x50 pixels

**AI Processing**:
1. Upload photo → Face detection runs
2. If no face found → Error message
3. If face found → Creates 128-dimensional encoding
4. Stores in database → Case becomes "Active"
5. Email confirmation sent (if email provided)

### 📸 **5. Reporting Sightings (Public Feature)**
**Requirements**: No login needed (anyone can report)  
**Click**: "Report Sighting"

**Upload Options**:
```
📁 File Upload:
- Images: JPEG, PNG, JPG
- Videos: MP4, AVI, MOV
- Max size: 10MB per file

📍 Location (Optional but Recommended):
- Click "Use Current Location" (GPS)
- OR enter coordinates manually
- OR enter location name (e.g., "Central Mall")

Example:
Location Name: Central Park, Mumbai
Latitude: 19.0760
Longitude: 72.8777
```

**AI Processing Flow**:
1. **Image Upload** → Face detection → Extract all faces
2. **Video Upload** → Sample 1 frame/second → Extract faces from each frame
3. **Face Matching** → Compare with all active cases
4. **If Match Found** (>60% similarity) → Email alert sent immediately
5. **Location Tracking** → GPS coordinates stored for timeline

### 📊 **6. My Cases Dashboard**
**Requirements**: Must be logged in  
**Click**: "My Cases"

**Features**:
```
📋 Case List View:
┌─────────────────────────────────────────┐
│ John Doe                    [Active]    │
│ 📸 [Photo]                              │
│ Created: Jan 15, 2024                   │
│ Contact: family@email.com               │
│ [Delete] [View Details]                 │
└─────────────────────────────────────────┘

Status Indicators:
🟡 Active - Currently searching
🟢 Found - Person located (admin marked)
```

**Actions Available**:
- ✅ View case details
- ✅ Delete case (removes from system)
- ✅ See creation date and contact info

### 👨💼 **7. Admin Dashboard**
**Requirements**: Admin account  
**Click**: "Admin Dashboard"

**Tab 1: Overview (Statistics)**
```
📊 System Statistics:
┌─────────────┬─────────────┬─────────────┐
│ Total Cases │ Active Cases│ Found Cases │
│     25      │     20      │      5      │
└─────────────┴─────────────┴─────────────┘
┌─────────────┬─────────────┬─────────────┐
│Total Sights │Total Matches│Pending Verif│
│    150      │     12      │      3      │
└─────────────┴─────────────┴─────────────┘
```

**Tab 2: Cases Management**
```
📋 All Missing Person Cases:
Name        Status    Created     Actions
John Doe    Active    Jan 15      [Mark Found] [View Locations]
Jane Smith  Found     Jan 10      [View Locations]
```

**Tab 3: Matches Verification**
```
🎯 Face Recognition Matches:
Person      Confidence  Location        Date      Actions
John Doe    87.3%      Central Park    Jan 20    [✓ Verify] [✗ Reject]
Jane Smith  92.1%      Mall Entrance   Jan 19    [✓ Verify] [✗ Reject]
```

**Tab 4: Location Tracking**
```
🗺️ Interactive Map View:
- Shows all sighting locations
- Click markers for details
- Timeline view of movements
- Confidence scores displayed
```

---

## 🤖 **AI & TECHNICAL FEATURES**

### 🧠 **Face Recognition Technology**

**Advanced Mode (if dlib available)**:
- Uses `face_recognition` library (dlib backend)
- 128-dimensional face encodings
- HOG + Linear SVM face detection
- Euclidean distance comparison
- 99.38% accuracy on LFW benchmark

**Fallback Mode (if dlib fails)**:
- Uses OpenCV Haar Cascades
- Histogram + edge feature extraction
- Cosine similarity comparison
- Still effective for basic matching

**Processing Pipeline**:
```
1. Image Input → Face Detection → Feature Extraction
2. Feature Vector → Database Storage (encrypted)
3. New Sighting → Face Extraction → Comparison
4. Similarity Score → Threshold Check → Alert Decision
```

### 📊 **Matching Algorithm**

**Similarity Calculation**:
```python
# Advanced (dlib)
face_distance = euclidean_distance(encoding1, encoding2)
similarity = 1 - face_distance

# Fallback (OpenCV)
similarity = cosine_similarity(features1, features2)
```

**Decision Logic**:
```
Similarity Score ≥ 0.6 (60%) = Match Found
Similarity Score < 0.6 (60%) = No Match

Configurable in .env:
FACE_MATCH_THRESHOLD=0.6
```

**Multi-Face Processing**:
- ✅ Detects multiple faces per image
- ✅ Processes each face separately
- ✅ Compares against all active cases
- ✅ Generates separate matches for each face

### 🎥 **Video Processing**

**Frame Sampling**:
```
Video Input → 1 frame per second extraction
Each Frame → Face detection → Face extraction
All Faces → Individual comparison → Match results
```

**Supported Formats**:
- MP4, AVI, MOV
- Max duration: Limited by file size (10MB)
- Processing time: ~30 seconds per minute of video

### 📧 **Email Notification System**

**Match Alert Email**:
```
Subject: ALERT: Possible sighting of John Doe

MISSING PERSON ALERT

A possible match has been found for: John Doe

Details:
- Confidence Score: 87.3%
- Location: Central Park, Mumbai
- Coordinates: 19.0760, 72.8777
- Time: 2024-01-20 14:30:25

Please verify this match as soon as possible.

[Attached: matched_face.jpg]
```

**Email Recipients**:
- Case creator (user who uploaded missing person)
- Contact email (if provided in case)
- Admin emails (configurable)

### 🗄️ **Database Schema**

**Users Table**:
```sql
id, email, phone, hashed_password, is_admin, created_at
```

**Missing Person Cases**:
```sql
id, name, address, aadhaar_hash, email, phone, 
photo_path, face_embedding, is_found, created_by, created_at
```

**Sightings**:
```sql
id, file_path, file_type, latitude, longitude, 
location_name, uploaded_at, processed
```

**Matches**:
```sql
id, case_id, sighting_id, confidence_score, 
matched_face_path, verified, created_at
```

**Location History**:
```sql
id, case_id, latitude, longitude, location_name, 
timestamp, confidence_score
```

---

## 🔒 **SECURITY & PRIVACY**

### 🛡️ **Data Protection**

**Password Security**:
- bcrypt hashing with salt
- Minimum 6 characters required
- No plain text storage

**Aadhaar Protection**:
```python
# Input: 1234-5678-9012
# Stored: SHA-256 hash (irreversible)
aadhaar_hash = hashlib.sha256("123456789012".encode()).hexdigest()
```

**JWT Authentication**:
```
Token expires: 30 minutes
Algorithm: HS256
Secret key: Configurable in .env
```

**File Upload Security**:
- File type validation
- Size limits (10MB)
- Malicious file detection
- Secure file naming

### 🔐 **API Security**

**CORS Protection**:
```python
allow_origins=["http://localhost:3000"]  # Only React app
allow_credentials=True
```

**Input Validation**:
- Pydantic schema validation
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection

---

## 📁 **PROJECT STRUCTURE EXPLAINED**

```
Missing Person/
├── 📄 README.md                    # Main documentation
├── 📄 START_HERE.md                # User guide
├── 📄 TECHNICAL_DESCRIPTION.md     # Technical specs
├── 📄 QUICK_GUIDE.md               # This file
├── 📄 setup.bat                    # Auto-setup script
├── 📄 docker-compose.yml           # Container orchestration
│
├── 📁 backend/                     # Python FastAPI Server
│   ├── 📄 main.py                  # FastAPI app entry point
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 .env                     # Configuration (auto-created)
│   │
│   ├── 📁 app/                     # Application code
│   │   ├── 📁 models/              # Database layer
│   │   │   ├── database.py         # DB connection & session
│   │   │   ├── models.py           # SQLAlchemy table models
│   │   │   └── schemas.py          # Pydantic validation schemas
│   │   │
│   │   ├── 📁 routes/              # API endpoints
│   │   │   ├── auth.py             # POST /auth/register, /auth/login
│   │   │   ├── cases.py            # POST /cases/, GET /cases/
│   │   │   ├── sightings.py        # POST /sightings/
│   │   │   └── admin.py            # GET /admin/stats, /admin/cases
│   │   │
│   │   ├── 📁 services/            # Business logic
│   │   │   └── background_tasks.py # Face matching processor
│   │   │
│   │   └── 📁 utils/               # Helper functions
│   │       ├── auth.py             # JWT token management
│   │       ├── face_recognition.py # AI face processing
│   │       └── email_service.py    # SMTP email sender
│   │
│   └── 📁 uploads/                 # File storage
│       ├── 📁 cases/               # Missing person photos
│       └── 📁 sightings/           # Uploaded sighting files
│
└── 📁 frontend/                    # React.js Web App
    ├── 📄 package.json             # Node.js dependencies
    │
    ├── 📁 public/                  # Static files
    │   └── index.html              # Main HTML template
    │
    └── 📁 src/                     # React source code
        ├── 📄 App.js               # Main app with routing
        ├── 📄 App.css              # Global styles
        │
        ├── 📁 components/          # Reusable UI components
        │   ├── Navbar.js           # Navigation bar
        │   └── MapComponent.js     # Leaflet map integration
        │
        ├── 📁 pages/               # Full page components
        │   ├── Home.js             # Landing page
        │   ├── Login.js            # User authentication
        │   ├── Register.js         # User registration
        │   ├── CreateCase.js       # Missing person form
        │   ├── MyCases.js          # User dashboard
        │   ├── UploadSighting.js   # Public sighting upload
        │   └── AdminDashboard.js   # Admin management
        │
        ├── 📁 services/            # API communication
        │   └── api.js              # Axios HTTP client
        │
        └── 📁 utils/               # Helper utilities
            └── AuthContext.js      # React authentication state
```

---

## 🚨 **TROUBLESHOOTING**

### ❌ **Common Issues & Solutions**

**1. "No face detected" error**
```
Problem: Face recognition can't find face in photo
Solutions:
✅ Use clearer photo with visible face
✅ Ensure good lighting
✅ Face should be at least 50x50 pixels
✅ Try different photo angle
```

**2. Email notifications not working**
```
Problem: Match alerts not being sent
Solutions:
✅ Check SMTP settings in backend\.env
✅ Verify Gmail app password (not regular password)
✅ Check spam/junk folder
✅ Test with different email provider
```

**3. Backend server won't start**
```
Problem: Python errors or port conflicts
Solutions:
✅ Check if port 8000 is already in use
✅ Verify Python 3.9+ is installed
✅ Delete backend\venv and run setup.bat again
✅ Check backend\.env configuration
```

**4. Frontend server won't start**
```
Problem: Node.js errors or port conflicts
Solutions:
✅ Check if port 3000 is already in use
✅ Verify Node.js 16+ is installed
✅ Delete frontend\node_modules and run setup.bat again
✅ Clear npm cache: npm cache clean --force
```

**5. Face matching not working**
```
Problem: No matches found for obvious matches
Solutions:
✅ Lower FACE_MATCH_THRESHOLD in .env (try 0.5)
✅ Use higher quality photos
✅ Ensure faces are similar angles/lighting
✅ Check if dlib installed properly
```

### 🔧 **Performance Optimization**

**For Better Face Recognition**:
- Use high-resolution photos (but under 10MB)
- Ensure faces are front-facing
- Good lighting conditions
- Minimal background distractions

**For Faster Processing**:
- Use images instead of videos when possible
- Compress large files before upload
- Use SSD storage for faster file access

---

## 📈 **SCALING & PRODUCTION**

### 🚀 **Production Deployment**

**Database Upgrade**:
```env
# Change from SQLite to PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/missing_persons
```

**Email Service Upgrade**:
```env
# Use professional email service
SMTP_SERVER=smtp.sendgrid.net
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

**File Storage Upgrade**:
- Local filesystem → AWS S3 / Google Cloud Storage
- CDN integration for faster image loading

**Security Enhancements**:
- HTTPS/SSL certificates
- Rate limiting
- Input sanitization
- Database encryption

### 📊 **Monitoring & Analytics**

**Metrics to Track**:
- Cases created per day
- Sightings uploaded per day
- Match accuracy rates
- Email delivery success
- System response times

**Log Analysis**:
- Face processing duration
- Database query performance
- Error rates by endpoint
- User activity patterns

---

## 🎯 **TESTING THE SYSTEM**

### 🧪 **Quick Test Workflow**

**Step 1: Create Test Case**
1. Register account: `test@example.com`
2. Login and create case: "Test Person"
3. Upload clear face photo
4. Verify case appears in "My Cases"

**Step 2: Test Sighting Upload**
1. Go to "Report Sighting" (no login needed)
2. Upload same person's photo (different angle)
3. Add location: "Test Location"
4. Submit and wait 30-60 seconds

**Step 3: Check Results**
1. Check email for match notification
2. Login as admin to verify match
3. Check location appears on map

**Sample Test Photos**:
- Use different photos of same person
- Try family member photos
- Test with group photos (multiple faces)

---

## 🆘 **SUPPORT & HELP**

### 📞 **Getting Help**

**Log Files Location**:
- Backend logs: Terminal window running backend
- Frontend logs: Browser developer console (F12)
- Database: `backend/missing_persons.db`

**Common Commands**:
```bash
# Restart everything
setup.bat

# Check Python version
python --version

# Check Node.js version
node --version

# Test backend directly
cd backend
call venv\Scripts\activate
python main.py

# Test frontend directly
cd frontend
npm start
```

**Performance Expectations**:
- Face processing: 5-30 seconds per image
- Video processing: 1-5 minutes per video
- Email delivery: 10-30 seconds
- Database queries: <100ms

---

## 🎉 **SUCCESS INDICATORS**

**✅ System Working Properly When**:
- Browser opens to http://localhost:3000 automatically
- Can register and login successfully
- Can create missing person case with photo
- Face detection works (no "no face found" errors)
- Can upload sightings without errors
- Email notifications arrive (check spam folder)
- Admin dashboard shows statistics
- Map displays sighting locations

**🎯 Ready to Help Find Missing Persons!**

The system is now fully operational and ready to assist in real missing person cases. All features are working end-to-end with AI-powered face recognition and instant alert notifications.