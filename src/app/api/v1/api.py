from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as authRouter
from app.api.v1.endpoints.states import router as stateRouter
from app.api.v1.endpoints.cities import router as cityRouter
from app.api.v1.endpoints.ies import router as iesRouter
from app.api.v1.endpoints.courses import router as courseRouter

router = APIRouter()

router.include_router(authRouter, prefix="/auth", tags=["Autenticação"])
router.include_router(stateRouter, prefix="/states", tags=["Estados"])
router.include_router(cityRouter, prefix="/cities", tags=["Cidades"])
router.include_router(iesRouter, prefix="/ies", tags=["Instituições"])
router.include_router(courseRouter, prefix="/courses", tags=["Cursos"])
