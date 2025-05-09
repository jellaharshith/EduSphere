from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from app.api.deps import get_db, get_current_user
from app.models.user import User, UserType
from app.schemas.user import UserInDB
from app.core.security import get_password_hash

router = APIRouter()

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Verify that the current user is an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

@router.get("/users", response_model=List[UserInDB])
def list_users(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(get_admin_user)
) -> Any:
    """
    List all users (admin only)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserInDB)
def get_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    _: User = Depends(get_admin_user)
) -> Any:
    """
    Get specific user details (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/users/{user_id}/deactivate")
def deactivate_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    _: User = Depends(get_admin_user)
) -> Any:
    """
    Deactivate a user account (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.is_active = False
    db.add(user)
    db.commit()
    return {"message": "User deactivated successfully"}

@router.post("/users/{user_id}/activate")
def activate_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    _: User = Depends(get_admin_user)
) -> Any:
    """
    Activate a user account (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.is_active = True
    db.add(user)
    db.commit()
    return {"message": "User activated successfully"}

@router.post("/users/{user_id}/reset-password")
def reset_user_password(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    new_password: str,
    _: User = Depends(get_admin_user)
) -> Any:
    """
    Reset a user's password (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    return {"message": "Password reset successfully"} 