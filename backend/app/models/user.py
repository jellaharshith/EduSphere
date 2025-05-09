from sqlalchemy import Boolean, Column, String, Integer, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class UserType(str, enum.Enum):
    STUDENT = "student"
    UNIVERSITY = "university"

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    user_type = Column(Enum(UserType), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    
    # Common profile fields
    profile_picture_url = Column(String(255))
    
    # Relationships
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    university_profile = relationship("UniversityProfile", back_populates="user", uselist=False)

class StudentProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    bio = Column(Text)
    education_level = Column(String(50))
    field_of_study = Column(String(100))
    skills = Column(Text)  # Stored as comma-separated values
    resume_url = Column(String(255))
    
    # Relationships
    user = relationship("User", back_populates="student_profile")
    applications = relationship("Application", back_populates="student")

class UniversityProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    location = Column(String(255))
    website = Column(String(255))
    accreditation = Column(String(255))
    
    # Relationships
    user = relationship("User", back_populates="university_profile")
    opportunities = relationship("Opportunity", back_populates="university") 