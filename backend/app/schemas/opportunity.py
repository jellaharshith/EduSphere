from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from app.models.opportunity import OpportunityType, ApplicationStatus

class OpportunityBase(BaseModel):
    title: str
    description: str
    type: OpportunityType
    location: Optional[str] = None
    is_remote: bool = False
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_weeks: Optional[int] = None
    stipend_amount: Optional[float] = None
    requirements: Optional[str] = None
    field_of_study: Optional[str] = None
    max_applications: Optional[int] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(OpportunityBase):
    is_active: Optional[bool] = None

class OpportunityInDB(OpportunityBase):
    id: int
    university_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    opportunity_id: int
    cover_letter: Optional[str] = None
    additional_info: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    cover_letter: Optional[str] = None
    additional_info: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    reviewer_notes: Optional[str] = None

class ApplicationInDB(ApplicationBase):
    id: int
    student_id: int
    status: ApplicationStatus
    reviewer_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Response models for listing opportunities with pagination
class OpportunitySearchParams(BaseModel):
    type: Optional[OpportunityType] = None
    location: Optional[str] = None
    is_remote: Optional[bool] = None
    field_of_study: Optional[str] = None
    min_stipend: Optional[float] = None
    start_date_after: Optional[date] = None
    keywords: Optional[str] = None

class OpportunityList(BaseModel):
    items: List[OpportunityInDB]
    total: int
    page: int
    size: int
    pages: int 