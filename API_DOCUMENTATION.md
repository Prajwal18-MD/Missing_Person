# API Documentation

## Base URL
- Development: `http://localhost:8000`
- Production: Update accordingly

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "phone": "+1234567890",
  "password": "securepassword"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```

### Missing Person Cases

#### Create Case
```http
POST /cases/
Authorization: Bearer <token>
Content-Type: multipart/form-data

name: John Doe
address: 123 Main St, City
aadhaar_number: 1234-5678-9012
email: contact@example.com
phone: +1234567890
photo: <file>
```

#### Get User Cases
```http
GET /cases/
Authorization: Bearer <token>
```

#### Get Specific Case
```http
GET /cases/{case_id}
Authorization: Bearer <token>
```

#### Update Case
```http
PUT /cases/{case_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "John Doe Updated",
  "address": "456 New St, City",
  "email": "newemail@example.com",
  "phone": "+0987654321"
}
```

#### Delete Case
```http
DELETE /cases/{case_id}
Authorization: Bearer <token>
```

### Sightings

#### Upload Sighting
```http
POST /sightings/
Content-Type: multipart/form-data

file: <image_or_video_file>
latitude: 28.6139
longitude: 77.2090
location_name: Central Park
```

#### Get All Sightings
```http
GET /sightings/
```

#### Get Specific Sighting
```http
GET /sightings/{sighting_id}
```

#### Reprocess Sighting
```http
POST /sightings/{sighting_id}/reprocess
```

### Admin Endpoints

#### Get Admin Statistics
```http
GET /admin/stats
Authorization: Bearer <admin_token>
```

Response:
```json
{
  "total_cases": 25,
  "active_cases": 20,
  "found_cases": 5,
  "total_sightings": 150,
  "total_matches": 12,
  "pending_matches": 3
}
```

#### Get All Cases (Admin)
```http
GET /admin/cases
Authorization: Bearer <admin_token>
```

#### Mark Person as Found
```http
PUT /admin/cases/{case_id}/found
Authorization: Bearer <admin_token>
```

#### Get All Matches
```http
GET /admin/matches?verified=false
Authorization: Bearer <admin_token>
```

#### Update Match Verification
```http
PUT /admin/matches/{match_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "verified": true
}
```

#### Get Location History
```http
GET /admin/cases/{case_id}/location-history
Authorization: Bearer <admin_token>
```

#### Delete Case (Admin)
```http
DELETE /admin/cases/{case_id}
Authorization: Bearer <admin_token>
```

## Error Responses

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

Error response format:
```json
{
  "detail": "Error message description"
}
```

## File Upload Limits
- Maximum file size: 10MB
- Supported image formats: JPEG, PNG, JPG
- Supported video formats: MP4, AVI, MOV

## Face Recognition
- Minimum face size: 50x50 pixels
- Confidence threshold: 0.6 (configurable)
- Supports multiple faces per image/video
- Video processing: 1 frame per second sampling