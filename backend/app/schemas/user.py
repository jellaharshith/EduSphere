from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.user import UserType
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    user_type: UserType

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class StudentProfileBase(BaseModel):
    first_name: str
    last_name: str
    bio: Optional[str] = None
    education_level: Optional[str] = None
    field_of_study: Optional[str] = None
    skills: Optional[str] = None

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfileUpdate(StudentProfileBase):
    pass

class StudentProfileInDB(StudentProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UniversityProfileBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    accreditation: Optional[str] = None

class UniversityProfileCreate(UniversityProfileBase):
    pass

class UniversityProfileUpdate(UniversityProfileBase):
    pass

class UniversityProfileInDB(UniversityProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    profile_picture_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    student_profile: Optional[StudentProfileInDB] = None
    university_profile: Optional[UniversityProfileInDB] = None

    class Config:
        from_attributes = True 