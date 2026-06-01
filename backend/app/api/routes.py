# app/api/routes.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.attorney_verifier import (
    verify_single_attorney
)

router = APIRouter()


class AttorneyRequest(BaseModel):

    name: str

    reg_no: str | None = None

    organization: str | None = None

    city: str | None = None


@router.post("/verify-attorney")
def verify_attorney_api(
    data: AttorneyRequest
):

    if not data.name.strip():

        return {
            "status": "error",
            "message": "Attorney name is required"
        }

    return verify_single_attorney(

        name=data.name,

        reg_no=data.reg_no or "",

        organization=data.organization or "",

        city=data.city or ""

    )