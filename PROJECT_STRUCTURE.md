# Missing Person Detection System - Project Structure

```
Missing Person/
├── README.md                           # Main project documentation
├── API_DOCUMENTATION.md               # API endpoints and examples
├── docker-compose.yml                 # Docker orchestration
├── setup.sh                          # Linux/Mac setup script
├── setup.bat                         # Windows setup script
│
├── backend/                           # Python FastAPI Backend
│   ├── main.py                       # FastAPI application entry point
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Backend Docker configuration
│   ├── .env.example                  # Environment variables template
│   │
│   ├── app/                          # Application package
│   │   ├── __init__.py
│   │   │
│   │   ├── models/                   # Database models and schemas
│   │   │   ├── __init__.py
│   │   │   ├── database.py           # Database connection setup
│   │   │   ├── models.py             # SQLAlchemy models
│   │   │   └── schemas.py            # Pydantic schemas
│   │   │
│   │   ├── routes/                   # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # Authentication routes
│   │   │   ├── cases.py              # Missing person case routes
│   │   │   ├── sightings.py          # Sighting upload routes
│   │   │   └── admin.py              # Admin dashboard routes
│   │   │
│   │   ├── services/                 # Business logic services
│   │   │   ├── __init__.py
│   │   │   └── background_tasks.py   # Face matching and processing
│   │   │
│   │   └── utils/                    # Utility functions
│   │       ├── __init__.py
│   │       ├── auth.py               # JWT and password utilities
│   │       ├── face_recognition.py   # Face detection and matching
│   │       └── email_service.py      # Email notification service
│   │
│   └── uploads/                      # File storage directory
│       ├── cases/                    # Missing person photos
│       └── sightings/                # Uploaded sighting files
│
├── frontend/                         # React.js Frontend
│   ├── package.json                  # Node.js dependencies
│   ├── Dockerfile                    # Frontend Docker configuration
│   │
│   ├── public/                       # Static files
│   │   └── index.html                # Main HTML template
│   │
│   └── src/                          # React source code
│       ├── index.js                  # React application entry point
│       ├── App.js                    # Main App component with routing
│       ├── App.css                   # Global styles
│       │
│       ├── components/               # Reusable React components
│       │   ├── Navbar.js             # Navigation bar
│       │   └── MapComponent.js       # Leaflet map integration
│       │
│       ├── pages/                    # Page components
│       │   ├── Home.js               # Landing page
│       │   ├── Login.js              # User login
│       │   ├── Register.js           # User registration
│       │   ├── CreateCase.js         # Create missing person case
│       │   ├── MyCases.js            # User's cases dashboard
│       │   ├── UploadSighting.js     # Public sighting upload
│       │   └── AdminDashboard.js     # Admin management interface
│       │
│       ├── services/                 # API communication
│       │   └── api.js                # Axios API client
│       │
│       └── utils/                    # Utility functions
│           └── AuthContext.js        # React authentication context
```

## Key Features by Component

### Backend Components

#### Database Models (`models/models.py`)
- **User**: Authentication and user management
- **MissingPersonCase**: Missing person information and face embeddings
- **Sighting**: Uploaded photos/videos with location data
- **Match**: Face recognition matches with confidence scores
- **LocationHistory**: Timeline of sighting locations

#### API Routes
- **Authentication** (`routes/auth.py`): Registration, login, JWT tokens
- **Cases** (`routes/cases.py`): CRUD operations for missing person cases
- **Sightings** (`routes/sightings.py`): File upload and processing
- **Admin** (`routes/admin.py`): Administrative functions and statistics

#### Core Services
- **Face Recognition** (`utils/face_recognition.py`): 
  - Face detection using dlib
  - Face encoding generation
  - Similarity comparison
  - Video frame extraction
- **Background Tasks** (`services/background_tasks.py`):
  - Asynchronous face matching
  - Email alert sending
  - Location history tracking
- **Email Service** (`utils/email_service.py`):
  - SMTP email notifications
  - Match alerts
  - Case status updates

### Frontend Components

#### Pages
- **Home**: Landing page with system overview
- **Authentication**: Login and registration forms
- **Case Management**: Create and manage missing person cases
- **Sighting Upload**: Public interface for reporting sightings
- **Admin Dashboard**: Statistics, case management, match verification

#### Components
- **Navbar**: Navigation with authentication state
- **MapComponent**: Interactive map using Leaflet/OpenStreetMap
- **AuthContext**: Global authentication state management

#### Services
- **API Client**: Axios-based HTTP client with authentication
- **Authentication**: JWT token management and user state

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Production database (SQLite for development)
- **face_recognition**: Face detection and recognition library
- **OpenCV**: Video processing and computer vision
- **JWT**: Secure authentication tokens
- **SMTP**: Email notifications

### Frontend
- **React.js**: Modern JavaScript UI framework
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Leaflet**: Interactive maps
- **CSS3**: Responsive styling

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **PostgreSQL**: Database service
- **Redis**: Caching and background tasks (optional)

## Security Features

1. **Password Hashing**: bcrypt for secure password storage
2. **JWT Authentication**: Secure token-based authentication
3. **Data Encryption**: Aadhaar numbers are hashed (SHA-256)
4. **File Validation**: Strict file type and size validation
5. **CORS Protection**: Configured for specific origins
6. **SQL Injection Prevention**: SQLAlchemy ORM protection
7. **Input Validation**: Pydantic schema validation

## Scalability Considerations

1. **Database Indexing**: Optimized queries with proper indexes
2. **File Storage**: Local filesystem (can be extended to S3/MinIO)
3. **Background Processing**: Async task processing
4. **Caching**: Redis integration ready
5. **Load Balancing**: Docker-ready for horizontal scaling
6. **API Rate Limiting**: Can be added with FastAPI middleware

## Deployment Options

1. **Development**: Local Python + Node.js
2. **Docker**: Single-machine deployment
3. **Production**: Kubernetes, AWS ECS, or similar
4. **Database**: PostgreSQL, MySQL, or cloud databases
5. **File Storage**: Local, AWS S3, Google Cloud Storage
6. **Email**: SMTP, SendGrid, AWS SES