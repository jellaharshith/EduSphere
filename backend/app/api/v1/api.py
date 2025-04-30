from fastapi import APIRouter
from app.api.v1.endpoints import auth, profiles, opportunities

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])

# Import and include other routers here
# from .endpoints import auth, users, etc.
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(users.router, prefix="/users", tags=["users"]) 