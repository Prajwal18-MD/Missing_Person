import os
from typing import List
from sqlalchemy.orm import Session
from ..models.database import SessionLocal
from ..models.models import Sighting, MissingPersonCase, Match, LocationHistory
from ..utils.face_recognition import FaceRecognitionService
from ..utils.email_service import EmailService
import numpy as np
from datetime import datetime

class BackgroundTaskService:
    def __init__(self):
        self.face_service = FaceRecognitionService()
        self.email_service = EmailService()
    
    def process_sighting(self, sighting_id: int):
        """Process a sighting and check for matches"""
        db = SessionLocal()
        try:
            # Get sighting
            sighting = db.query(Sighting).filter(Sighting.id == sighting_id).first()
            if not sighting:
                return
            
            # Create output directory for extracted faces
            sighting_dir = os.path.join("uploads", "sightings", f"sighting_{sighting_id}")
            os.makedirs(sighting_dir, exist_ok=True)
            
            extracted_faces = []
            
            # Process based on file type
            if sighting.file_type == "image":
                extracted_faces = self.face_service.process_sighting_image(
                    sighting.file_path, sighting_dir
                )
            elif sighting.file_type == "video":
                extracted_faces = self.face_service.extract_faces_from_video(
                    sighting.file_path, sighting_dir
                )
            
            # Check each extracted face against all active cases
            for face_path in extracted_faces:
                face_encoding = self.face_service.extract_face_encoding(face_path)
                if face_encoding is not None:
                    self._check_face_against_cases(db, face_encoding, sighting, face_path)
            
            # Mark sighting as processed
            sighting.processed = True
            db.commit()
            
        except Exception as e:
            print(f"Error processing sighting {sighting_id}: {e}")
            db.rollback()
        finally:
            db.close()
    
    def _check_face_against_cases(
        self, 
        db: Session, 
        face_encoding: np.ndarray, 
        sighting: Sighting, 
        face_path: str
    ):
        """Check a face encoding against all active missing person cases"""
        # Get all active cases (not found)
        active_cases = db.query(MissingPersonCase).filter(
            MissingPersonCase.is_found == False,
            MissingPersonCase.face_embedding.isnot(None)
        ).all()
        
        for case in active_cases:
            try:
                # Deserialize stored face encoding
                stored_encoding = self.face_service.deserialize_encoding(case.face_embedding)
                
                # Compare faces
                similarity_score = self.face_service.compare_faces(stored_encoding, face_encoding)
                
                # Check if it's a match
                if self.face_service.is_match(similarity_score):
                    # Create match record
                    match = Match(
                        case_id=case.id,
                        sighting_id=sighting.id,
                        confidence_score=similarity_score,
                        matched_face_path=face_path
                    )
                    db.add(match)
                    
                    # Add location to history if available
                    if sighting.latitude and sighting.longitude:
                        location_history = LocationHistory(
                            case_id=case.id,
                            latitude=sighting.latitude,
                            longitude=sighting.longitude,
                            location_name=sighting.location_name,
                            confidence_score=similarity_score
                        )
                        db.add(location_history)
                    
                    db.commit()
                    
                    # Send email alert
                    self._send_match_alert(case, sighting, similarity_score, face_path)
                    
            except Exception as e:
                print(f"Error checking case {case.id}: {e}")
                continue
    
    def _send_match_alert(
        self, 
        case: MissingPersonCase, 
        sighting: Sighting, 
        confidence_score: float, 
        face_path: str
    ):
        """Send email alert for a match"""
        try:
            # Prepare email recipients
            to_emails = []
            if case.email:
                to_emails.append(case.email)
            if case.created_by_user and case.created_by_user.email:
                to_emails.append(case.created_by_user.email)
            
            # Prepare location info
            location = "Unknown location"
            if sighting.location_name:
                location = sighting.location_name
            elif sighting.latitude and sighting.longitude:
                location = f"Lat: {sighting.latitude}, Lng: {sighting.longitude}"
            
            # Send alert
            if to_emails:
                self.email_service.send_match_alert(
                    to_emails=to_emails,
                    missing_person_name=case.name,
                    confidence_score=confidence_score,
                    location=location,
                    timestamp=sighting.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
                    matched_image_path=face_path
                )
                
        except Exception as e:
            print(f"Error sending match alert: {e}")

# Global instance
background_service = BackgroundTaskService()