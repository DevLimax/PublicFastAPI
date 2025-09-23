from fastapi import APIRouter

from publicapi.api.v1.endpoints.auth import router as authRouter

router = APIRouter()

router.include_router(authRouter, prefix="/auth", tags=["Autenticação"])
