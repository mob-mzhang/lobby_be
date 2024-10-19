from fastapi import APIRouter
from .ops import matchmaking, lobbys_ops, users_ops


router = APIRouter()
router.include_router(matchmaking.router, tags=["matchmaking"])
router.include_router(lobbys_ops.router, tags=["lobbys"])
router.include_router(users_ops.router, tags=["users"])

