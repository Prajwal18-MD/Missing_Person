from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime

from ..models.database import get_db
from ..models.models import User, MissingPersonCase
from ..models.schemas import MissingPersonCaseCreate, MissingPersonCase as MissingPersonCaseSchema
from ..utils.auth import get_current_user
from ..utils.face_recognition import FaceRecognitionService
from ..utils.email_service import EmailService

router = APIRouter()
face_service = FaceRecognitionService()
email_service = EmailService()

@router.post("/", response_model=MissingPersonCaseSchema)
async def create_missing_person_case(
    name: str = Form(...),
    address: Optional[str] = Form(None),
    aadhaar_number: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    if not photo.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed"
        )
    
    # Create case directory
    case_dir = os.path.join("uploads", "cases")
    os.makedirs(case_dir, exist_ok=True)
    
    # Save uploaded photo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_filename = f"{timestamp}_{photo.filename}"
    photo_path = os.path.join(case_dir, photo_filename)
    
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    
    # Extract face encoding
    face_encoding = face_service.extract_face_encoding(photo_path)
    if face_encoding is None:
        # Clean up uploaded file
        os.remove(photo_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No face detected in the uploaded photo. Please upload a clear photo with a visible face."
        )
    
    # Create missing person case
    db_case = MissingPersonCase(
        name=name,
        address=address,
        email=email,
        phone=phone,
        photo_path=photo_path,
        face_embedding=face_service.serialize_encoding(face_encoding),
        created_by=current_user.id
    )
    
    # Hash Aadhaar if provided
    if aadhaar_number:
        db_case.set_aadhaar(aadhaar_number)
    
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    
    # Send confirmation email
    if email:
        email_service.send_case_created_notification(email, name, db_case.id)
    
    return db_case

@router.get("/", response_model=List[MissingPersonCaseSchema])
async def get_user_cases(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cases = db.query(MissingPersonCase).filter(
        MissingPersonCase.created_by == current_user.id
    ).all()
    return cases

@router.get("/{case_id}", response_model=MissingPersonCaseSchema)
async def get_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    case = db.query(MissingPersonCase).filter(
        MissingPersonCase.id == case_id,
        MissingPersonCase.created_by == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    return case

@router.put("/{case_id}", response_model=MissingPersonCaseSchema)
async def update_case(
    case_id: int,
    case_update: MissingPersonCaseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    case = db.query(MissingPersonCase).filter(
        MissingPersonCase.id == case_id,
        MissingPersonCase.created_by == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Update fields
    case.name = case_update.name
    case.address = case_update.address
    case.email = case_update.email
    case.phone = case_update.phone
    
    if case_update.aadhaar_number:
        case.set_aadhaar(case_update.aadhaar_number)
    
    db.commit()
    db.refresh(case)
    
    return case

@router.delete("/{case_id}")
async def delete_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    case = db.query(MissingPersonCase).filter(
        MissingPersonCase.id == case_id,
        MissingPersonCase.created_by == current_user.id
    ).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Delete photo file
    if os.path.exists(case.photo_path):
        os.remove(case.photo_path)
    
    db.delete(case)
    db.commit()
    
    return {"message": "Case deleted successfully"}