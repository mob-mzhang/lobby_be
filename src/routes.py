from fastapi import APIRouter
from .ops.users_ops import router as users_router
from .ops.events_ops import router as events_router
from src.upload import router as upload_router
from .auth import router as auth_router  # Add this line

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(events_router, prefix="/events", tags=["events"])
router.include_router(upload_router, prefix="/upload", tags=["upload"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])  # Add this line