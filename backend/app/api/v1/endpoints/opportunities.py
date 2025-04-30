from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Any, List
from app.api.deps import get_db, get_current_university, get_current_student, get_current_user
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityUpdate,
    OpportunityInDB,
    OpportunityList,
    OpportunitySearchParams,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationInDB
)
from app.models.opportunity import Opportunity, Application, ApplicationStatus
from app.models.user import User
from datetime import date
import openai
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Opportunity Management Endpoints
@router.post("/", response_model=OpportunityInDB)
def create_opportunity(
    *,
    db: Session = Depends(get_db),
    opportunity_in: OpportunityCreate,
    current_user: User = Depends(get_current_university)
) -> Any:
    """
    Create new opportunity.
    """
    db_opportunity = Opportunity(
        university_id=current_user.university_profile.id,
        **opportunity_in.model_dump()
    )
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity

@router.put("/{opportunity_id}", response_model=OpportunityInDB)
def update_opportunity(
    *,
    db: Session = Depends(get_db),
    opportunity_id: int,
    opportunity_in: OpportunityUpdate,
    current_user: User = Depends(get_current_university)
) -> Any:
    """
    Update opportunity.
    """
    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opportunity_id,
        Opportunity.university_id == current_user.university_profile.id
    ).first()
    
    if not opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    
    for field, value in opportunity_in.model_dump(exclude_unset=True).items():
        setattr(opportunity, field, value)
    
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    return opportunity

@router.get("/search", response_model=OpportunityList)
def search_opportunities(
    *,
    db: Session = Depends(get_db),
    params: OpportunitySearchParams = Depends(),
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100)
) -> Any:
    """
    Search opportunities with filters and pagination.
    """
    query = db.query(Opportunity).filter(Opportunity.is_active == True)
    
    # Apply filters
    if params.type:
        query = query.filter(Opportunity.type == params.type)
    if params.location:
        query = query.filter(Opportunity.location.ilike(f"%{params.location}%"))
    if params.is_remote is not None:
        query = query.filter(Opportunity.is_remote == params.is_remote)
    if params.field_of_study:
        query = query.filter(Opportunity.field_of_study.ilike(f"%{params.field_of_study}%"))
    if params.min_stipend:
        query = query.filter(Opportunity.stipend_amount >= params.min_stipend)
    if params.start_date_after:
        query = query.filter(Opportunity.start_date >= params.start_date_after)
    if params.keywords:
        query = query.filter(
            or_(
                Opportunity.title.ilike(f"%{params.keywords}%"),
                Opportunity.description.ilike(f"%{params.keywords}%")
            )
        )
    
    # Calculate pagination
    total = query.count()
    pages = (total + size - 1) // size
    
    items = query.offset((page - 1) * size).limit(size).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }

# Application Management Endpoints
@router.post("/apply/{opportunity_id}", response_model=ApplicationInDB)
def create_application(
    *,
    db: Session = Depends(get_db),
    opportunity_id: int,
    application_in: ApplicationCreate,
    current_user: User = Depends(get_current_student)
) -> Any:
    """
    Create new application for an opportunity.
    """
    # Check if opportunity exists and is active
    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opportunity_id,
        Opportunity.is_active == True
    ).first()
    
    if not opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found or inactive"
        )
    
    # Check if student has already applied
    existing_application = db.query(Application).filter(
        Application.student_id == current_user.student_profile.id,
        Application.opportunity_id == opportunity_id
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already applied to this opportunity"
        )
    
    db_application = Application(
        student_id=current_user.student_profile.id,
        status=ApplicationStatus.SUBMITTED,
        **application_in.model_dump()
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@router.put("/applications/{application_id}", response_model=ApplicationInDB)
def update_application_status(
    *,
    db: Session = Depends(get_db),
    application_id: int,
    application_in: ApplicationUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update application status and notes.
    """
    application = db.query(Application).filter(Application.id == application_id)
    
    # Add user type specific filters
    if current_user.user_type == "student":
        application = application.filter(Application.student_id == current_user.student_profile.id)
    else:  # university
        application = application.join(Opportunity).filter(
            Opportunity.university_id == current_user.university_profile.id
        )
    
    application = application.first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Students can only update their application if it's in DRAFT status
    if current_user.user_type == "student" and application.status != ApplicationStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify submitted application"
        )
    
    for field, value in application_in.model_dump(exclude_unset=True).items():
        setattr(application, field, value)
    
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

@router.get("/recommendations", response_model=List[OpportunityInDB])
async def get_recommendations(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
) -> Any:
    """
    Get AI-powered opportunity recommendations for student.
    """
    if not current_user.student_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student profile not found"
        )
    
    # Prepare student profile data
    student = current_user.student_profile
    profile_text = f"""
    Student studying {student.field_of_study} at {student.education_level} level.
    Skills: {student.skills}
    """
    
    # Get active opportunities
    opportunities = db.query(Opportunity).filter(Opportunity.is_active == True).all()
    
    try:
        # Use OpenAI to rank opportunities
        openai.api_key = settings.OPENAI_API_KEY
        response = await openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career advisor helping match students with opportunities."},
                {"role": "user", "content": f"Given this student profile:\n{profile_text}\n\nRank these opportunities from most to least relevant (return only opportunity IDs in order):\n" + "\n".join([f"ID {opp.id}: {opp.title} - {opp.description}" for opp in opportunities])}
            ]
        )
        
        # Extract recommended opportunity IDs
        recommended_ids = [int(id_str) for id_str in response.choices[0].message.content.split() if id_str.isdigit()]
        
        # Get recommended opportunities in order
        recommended = []
        for opp_id in recommended_ids[:5]:  # Return top 5 recommendations
            opp = next((o for o in opportunities if o.id == opp_id), None)
            if opp:
                recommended.append(opp)
        
        return recommended
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )

@router.get("/")
async def get_opportunities(token: str = Depends(oauth2_scheme)):
    # TODO: Implement actual opportunities retrieval
    return {"message": "Get all opportunities"}

@router.get("/{opportunity_id}")
async def get_opportunity(opportunity_id: int, token: str = Depends(oauth2_scheme)):
    # TODO: Implement actual opportunity retrieval
    return {"message": f"Get opportunity {opportunity_id}"} 