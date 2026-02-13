from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import hashlib

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    cases = relationship("MissingPersonCase", back_populates="created_by_user")

class MissingPersonCase(Base):
    __tablename__ = "missing_person_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(Text)
    aadhaar_hash = Column(String)  # Store hashed Aadhaar
    email = Column(String)
    phone = Column(String)
    photo_path = Column(String, nullable=False)
    face_embedding = Column(LargeBinary)  # Store face embedding as binary
    is_found = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    created_by_user = relationship("User", back_populates="cases")
    matches = relationship("Match", back_populates="case")
    location_history = relationship("LocationHistory", back_populates="case")
    
    def set_aadhaar(self, aadhaar_number):
        """Hash and store Aadhaar number"""
        if aadhaar_number:
            self.aadhaar_hash = hashlib.sha256(aadhaar_number.encode()).hexdigest()

class Sighting(Base):
    __tablename__ = "sightings"
    
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # 'image' or 'video'
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed = Column(Boolean, default=False)
    
    # Relationships
    matches = relationship("Match", back_populates="sighting")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("missing_person_cases.id"))
    sighting_id = Column(Integer, ForeignKey("sightings.id"))
    confidence_score = Column(Float, nullable=False)
    matched_face_path = Column(String)  # Path to extracted face image
    verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    case = relationship("MissingPersonCase", back_populates="matches")
    sighting = relationship("Sighting", back_populates="matches")
    verified_by_user = relationship("User")

class LocationHistory(Base):
    __tablename__ = "location_history"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("missing_person_cases.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_name = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    confidence_score = Column(Float)  # From the match that created this location
    
    # Relationships
    case = relationship("MissingPersonCase", back_populates="location_history")