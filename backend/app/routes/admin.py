from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from ..models.database import get_db
from ..models.models import User, MissingPersonCase, Sighting, Match, LocationHistory
from ..models.schemas import (
    MissingPersonCase as MissingPersonCaseSchema,
    Match as MatchSchema,
    MatchUpdate,
    AdminStats,
    LocationHistory as LocationHistorySchema
)
from ..utils.auth import get_admin_user
from ..utils.email_service import EmailService

router = APIRouter()
email_service = EmailService()

@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    total_cases = db.query(MissingPersonCase).count()
    active_cases = db.query(MissingPersonCase).filter(MissingPersonCase.is_found == False).count()
    found_cases = db.query(MissingPersonCase).filter(MissingPersonCase.is_found == True).count()
    total_sightings = db.query(Sighting).count()
    total_matches = db.query(Match).count()
    pending_matches = db.query(Match).filter(Match.verified == False).count()
    
    return AdminStats(
        total_cases=total_cases,
        active_cases=active_cases,
        found_cases=found_cases,
        total_sightings=total_sightings,
        total_matches=total_matches,
        pending_matches=pending_matches
    )

@router.get("/cases", response_model=List[MissingPersonCaseSchema])
async def get_all_cases(
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    cases = db.query(MissingPersonCase).offset(skip).limit(limit).all()
    return cases

@router.get("/cases/{case_id}", response_model=MissingPersonCaseSchema)
async def get_case_details(
    case_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    case = db.query(MissingPersonCase).filter(MissingPersonCase.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    return case

@router.put("/cases/{case_id}/found")
async def mark_person_found(
    case_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    case = db.query(MissingPersonCase).filter(MissingPersonCase.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    if case.is_found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Person is already marked as found"
        )
    
    # Mark as found
    case.is_found = True
    db.commit()
    
    # Send notification emails
    to_emails = []
    if case.email:
        to_emails.append(case.email)
    if case.created_by_user and case.created_by_user.email:
        to_emails.append(case.created_by_user.email)
    
    if to_emails:
        email_service.send_person_found_notification(to_emails, case.name, case.id)
    
    return {"message": f"{case.name} has been marked as found"}

@router.get("/matches", response_model=List[MatchSchema])
async def get_all_matches(
    skip: int = 0,
    limit: int = 100,
    verified: bool = None,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    query = db.query(Match)
    
    if verified is not None:
        query = query.filter(Match.verified == verified)
    
    matches = query.offset(skip).limit(limit).all()
    return matches

@router.put("/matches/{match_id}", response_model=MatchSchema)
async def update_match(
    match_id: int,
    match_update: MatchUpdate,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    match.verified = match_update.verified
    match.verified_by = admin_user.id
    db.commit()
    db.refresh(match)
    
    return match

@router.get("/cases/{case_id}/location-history", response_model=List[LocationHistorySchema])
async def get_case_location_history(
    case_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    # Verify case exists
    case = db.query(MissingPersonCase).filter(MissingPersonCase.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Get location history
    locations = db.query(LocationHistory).filter(
        LocationHistory.case_id == case_id
    ).order_by(LocationHistory.timestamp.desc()).all()
    
    return locations

@router.delete("/cases/{case_id}")
async def delete_case(
    case_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    case = db.query(MissingPersonCase).filter(MissingPersonCase.id == case_id).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Delete associated records first
    db.query(LocationHistory).filter(LocationHistory.case_id == case_id).delete()
    db.query(Match).filter(Match.case_id == case_id).delete()
    
    # Delete photo file
    import os
    if os.path.exists(case.photo_path):
        os.remove(case.photo_path)
    
    # Delete case
    db.delete(case)
    db.commit()
    
    return {"message": "Case deleted successfully"}