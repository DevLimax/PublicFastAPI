from fastapi import APIRouter

from publicapi.api.v1.endpoints.auth import router as authRouter
from publicapi.api.v1.endpoints.states import router as stateRouter

router = APIRouter()

router.include_router(authRouter, prefix="/auth", tags=["Autenticação"])
router.include_router(stateRouter, prefix="/states", tags=["Estados"])