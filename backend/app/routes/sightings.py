from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime

from ..models.database import get_db
from ..models.models import Sighting
from ..models.schemas import SightingCreate, Sighting as SightingSchema
from ..services.background_tasks import background_service

router = APIRouter()

@router.post("/", response_model=SightingSchema)
async def upload_sighting(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    location_name: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'video/mp4', 'video/avi', 'video/mov']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image (JPEG, PNG) and video (MP4, AVI, MOV) files are allowed"
        )
    
    # Determine file type
    file_type = "image" if file.content_type.startswith('image/') else "video"
    
    # Create sighting directory
    sighting_dir = os.path.join("uploads", "sightings")
    os.makedirs(sighting_dir, exist_ok=True)
    
    # Save uploaded file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    filename = f"sighting_{timestamp}.{file_extension}"
    file_path = os.path.join(sighting_dir, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create sighting record
    db_sighting = Sighting(
        file_path=file_path,
        file_type=file_type,
        latitude=latitude,
        longitude=longitude,
        location_name=location_name
    )
    
    db.add(db_sighting)
    db.commit()
    db.refresh(db_sighting)
    
    # Add background task to process the sighting
    background_tasks.add_task(background_service.process_sighting, db_sighting.id)
    
    return db_sighting

@router.get("/", response_model=List[SightingSchema])
async def get_sightings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    sightings = db.query(Sighting).offset(skip).limit(limit).all()
    return sightings

@router.get("/{sighting_id}", response_model=SightingSchema)
async def get_sighting(
    sighting_id: int,
    db: Session = Depends(get_db)
):
    sighting = db.query(Sighting).filter(Sighting.id == sighting_id).first()
    if not sighting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sighting not found"
        )
    return sighting

@router.post("/{sighting_id}/reprocess")
async def reprocess_sighting(
    sighting_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    sighting = db.query(Sighting).filter(Sighting.id == sighting_id).first()
    if not sighting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sighting not found"
        )
    
    # Reset processed status
    sighting.processed = False
    db.commit()
    
    # Add background task to reprocess
    background_tasks.add_task(background_service.process_sighting, sighting_id)
    
    return {"message": "Sighting queued for reprocessing"}