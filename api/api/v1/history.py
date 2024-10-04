from fastapi import APIRouter, Depends, status

from functions import api_key_required


version_1_history_router = APIRouter(
    prefix="/api/v1/history",
    tags=["History"],
    dependencies=[Depends(api_key_required)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API Key"}},
)
