from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: str
    phone: str
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Missing Person Case schemas
class MissingPersonCaseCreate(BaseModel):
    name: str
    address: Optional[str] = None
    aadhaar_number: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class MissingPersonCase(BaseModel):
    id: int
    name: str
    address: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    photo_path: str
    is_found: bool
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

# Sighting schemas
class SightingCreate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: Optional[str] = None

class Sighting(BaseModel):
    id: int
    file_path: str
    file_type: str
    latitude: Optional[float]
    longitude: Optional[float]
    location_name: Optional[str]
    uploaded_at: datetime
    processed: bool
    
    class Config:
        from_attributes = True

# Match schemas
class Match(BaseModel):
    id: int
    case_id: int
    sighting_id: int
    confidence_score: float
    matched_face_path: Optional[str]
    verified: bool
    created_at: datetime
    case: MissingPersonCase
    sighting: Sighting
    
    class Config:
        from_attributes = True

class MatchUpdate(BaseModel):
    verified: bool

# Location History schemas
class LocationHistory(BaseModel):
    id: int
    case_id: int
    latitude: float
    longitude: float
    location_name: Optional[str]
    timestamp: datetime
    confidence_score: Optional[float]
    
    class Config:
        from_attributes = True

# Admin schemas
class AdminStats(BaseModel):
    total_cases: int
    active_cases: int
    found_cases: int
    total_sightings: int
    total_matches: int
    pending_matches: int