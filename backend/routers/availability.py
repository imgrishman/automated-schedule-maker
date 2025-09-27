from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional

from models.availability import AvailabilityCreate, AvailabilityUpdate, Availability
from models.user import UserInDB
from services.availability_service import AvailabilityService
from middleware.auth import get_current_user, get_current_admin_user

router = APIRouter()

@router.post("/", response_model=Availability)
async def create_availability(
    availability_data: AvailabilityCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        availability = await AvailabilityService.create_availability(availability_data)
        return Availability(
            id=str(availability.id),
            employee_id=availability.employee_id,
            weekly_availability=availability.weekly_availability,
            max_hours_per_week=availability.max_hours_per_week,
            preferred_shift_length=availability.preferred_shift_length,
            notes=availability.notes,
            effective_date=availability.effective_date,
            created_at=availability.created_at,
            updated_at=availability.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/employee/{employee_id}", response_model=Optional[Availability])
async def get_employee_availability(
    employee_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    availability = await AvailabilityService.get_current_availability(employee_id)
    if not availability:
        return None
    
    return Availability(
        id=str(availability.id),
        employee_id=availability.employee_id,
        weekly_availability=availability.weekly_availability,
        max_hours_per_week=availability.max_hours_per_week,
        preferred_shift_length=availability.preferred_shift_length,
        notes=availability.notes,
        effective_date=availability.effective_date,
        created_at=availability.created_at,
        updated_at=availability.updated_at
    )

@router.get("/", response_model=List[Availability])
async def get_all_availability(
    current_user: UserInDB = Depends(get_current_admin_user)
):
    availabilities = await AvailabilityService.get_all_availability()
    return [
        Availability(
            id=str(avail.id),
            employee_id=avail.employee_id,
            weekly_availability=avail.weekly_availability,
            max_hours_per_week=avail.max_hours_per_week,
            preferred_shift_length=avail.preferred_shift_length,
            notes=avail.notes,
            effective_date=avail.effective_date,
            created_at=avail.created_at,
            updated_at=avail.updated_at
        )
        for avail in availabilities
    ]

@router.put("/{availability_id}", response_model=Availability)
async def update_availability(
    availability_id: str,
    availability_data: AvailabilityUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    availability = await AvailabilityService.update_availability(availability_id, availability_data)
    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability not found"
        )
    
    return Availability(
        id=str(availability.id),
        employee_id=availability.employee_id,
        weekly_availability=availability.weekly_availability,
        max_hours_per_week=availability.max_hours_per_week,
        preferred_shift_length=availability.preferred_shift_length,
        notes=availability.notes,
        effective_date=availability.effective_date,
        created_at=availability.created_at,
        updated_at=availability.updated_at
    )
