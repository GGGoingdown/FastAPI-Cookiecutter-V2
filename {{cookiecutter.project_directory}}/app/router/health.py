from fastapi import APIRouter

from app.schema import GenericSchema

router = APIRouter(tags=["Health check"])


@router.get("/health", response_model=GenericSchema.DetailResponse)
async def health_check():
    return {"detail": "ok"}
