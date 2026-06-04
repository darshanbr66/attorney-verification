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

    # -----------------------------
    # NAME VALIDATION
    # -----------------------------

    if not data.name.strip():

        return {
            "status": "error",
            "message": "Attorney name is required"
        }

    # -----------------------------
    # ORG OR CITY VALIDATION
    # -----------------------------

    has_organization = (
        data.organization
        and data.organization.strip()
    )

    has_city = (
        data.city
        and data.city.strip()
    )

    if not has_organization and not has_city:

        return {
            "status": "error",
            "message":
            "Please provide either Organization or City along with Attorney Name"
        }

    # -----------------------------
    # START VERIFICATION
    # -----------------------------

    return verify_single_attorney(

        name=data.name.strip(),

        reg_no=(
            data.reg_no.strip()
            if data.reg_no
            else ""
        ),

        organization=(
            data.organization.strip()
            if data.organization
            else ""
        ),

        city=(
            data.city.strip()
            if data.city
            else ""
        )

    )