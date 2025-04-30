from sqlalchemy import Boolean, Column, String, Integer, Enum, Text, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class OpportunityType(str, enum.Enum):
    INTERNSHIP = "internship"
    RESEARCH = "research"

class ApplicationStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Opportunity(Base):
    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universityprofile.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(Enum(OpportunityType), nullable=False)
    location = Column(String(255))
    is_remote = Column(Boolean, default=False)
    start_date = Column(Date)
    end_date = Column(Date)
    duration_weeks = Column(Integer)
    stipend_amount = Column(Float)
    requirements = Column(Text)
    field_of_study = Column(String(100))
    is_active = Column(Boolean, default=True)
    max_applications = Column(Integer)
    
    # Relationships
    university = relationship("UniversityProfile", back_populates="opportunities")
    applications = relationship("Application", back_populates="opportunity")

class Application(Base):
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("studentprofile.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunity.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT)
    cover_letter = Column(Text)
    additional_info = Column(Text)
    reviewer_notes = Column(Text)
    
    # Relationships
    student = relationship("StudentProfile", back_populates="applications")
    opportunity = relationship("Opportunity", back_populates="applications") 