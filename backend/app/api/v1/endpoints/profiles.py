from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Any, List
from app.api.deps import get_db, get_current_user, get_current_student, get_current_university
from app.schemas.user import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileInDB,
    UniversityProfileCreate,
    UniversityProfileUpdate,
    UniversityProfileInDB,
)
from app.models.user import User, UserType, StudentProfile, UniversityProfile
import boto3
from app.core.config import settings
import uuid
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Student Profile Endpoints
@router.post("/student", response_model=StudentProfileInDB)
def create_student_profile(
    *,
    db: Session = Depends(get_db),
    profile_in: StudentProfileCreate,
    current_user: User = Depends(get_current_student)
) -> Any:
    """
    Create new student profile.
    """
    if current_user.student_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student profile already exists"
        )
    
    db_profile = StudentProfile(
        user_id=current_user.id,
        **profile_in.model_dump()
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.put("/student", response_model=StudentProfileInDB)
def update_student_profile(
    *,
    db: Session = Depends(get_db),
    profile_in: StudentProfileUpdate,
    current_user: User = Depends(get_current_student)
) -> Any:
    """
    Update student profile.
    """
    if not current_user.student_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    for field, value in profile_in.model_dump(exclude_unset=True).items():
        setattr(current_user.student_profile, field, value)
    
    db.add(current_user.student_profile)
    db.commit()
    db.refresh(current_user.student_profile)
    return current_user.student_profile

# University Profile Endpoints
@router.post("/university", response_model=UniversityProfileInDB)
def create_university_profile(
    *,
    db: Session = Depends(get_db),
    profile_in: UniversityProfileCreate,
    current_user: User = Depends(get_current_university)
) -> Any:
    """
    Create new university profile.
    """
    if current_user.university_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="University profile already exists"
        )
    
    db_profile = UniversityProfile(
        user_id=current_user.id,
        **profile_in.model_dump()
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.put("/university", response_model=UniversityProfileInDB)
def update_university_profile(
    *,
    db: Session = Depends(get_db),
    profile_in: UniversityProfileUpdate,
    current_user: User = Depends(get_current_university)
) -> Any:
    """
    Update university profile.
    """
    if not current_user.university_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="University profile not found"
        )
    
    for field, value in profile_in.model_dump(exclude_unset=True).items():
        setattr(current_user.university_profile, field, value)
    
    db.add(current_user.university_profile)
    db.commit()
    db.refresh(current_user.university_profile)
    return current_user.university_profile

# Profile Picture Upload Endpoint
@router.post("/upload-picture")
async def upload_profile_picture(
    *,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Upload profile picture to S3 and update user profile.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Initialize S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    filename = f"profile-pictures/{current_user.id}/{uuid.uuid4()}.{file_extension}"
    
    try:
        # Upload file to S3
        s3_client.upload_fileobj(
            file.file,
            settings.AWS_BUCKET_NAME,
            filename,
            ExtraArgs={"ContentType": file.content_type}
        )
        
        # Update user profile with new picture URL
        current_user.profile_picture_url = f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{filename}"
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        
        return {"url": current_user.profile_picture_url}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/")
async def get_profiles(token: str = Depends(oauth2_scheme)):
    # TODO: Implement actual profile retrieval
    return {"message": "Get all profiles"}

@router.get("/{profile_id}")
async def get_profile(profile_id: int, token: str = Depends(oauth2_scheme)):
    # TODO: Implement actual profile retrieval
    return {"message": f"Get profile {profile_id}"} 