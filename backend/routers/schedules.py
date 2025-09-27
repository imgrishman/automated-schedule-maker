from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from typing import List

from models.schedule import (
    ScheduleCreate, ScheduleUpdate, Schedule, ScheduleWithShifts, 
    ScheduleGenerationRequest, Shift
)
from models.user import UserInDB
from services.schedule_service import ScheduleService
from middleware.auth import get_current_admin_user, get_current_user

router = APIRouter()

@router.post("/generate")
async def generate_schedule(
    request: ScheduleGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    try:
        # Start background task for AI schedule generation
        schedule_id = await ScheduleService.start_schedule_generation(request, str(current_user.id))
        
        return {
            "success": True,
            "message": "Schedule generation started",
            "schedule_id": schedule_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[Schedule])
async def get_all_schedules(
    current_user: UserInDB = Depends(get_current_admin_user)
):
    schedules = await ScheduleService.get_all_schedules()
    return [
        Schedule(
            id=str(schedule.id),
            name=schedule.name,
            week_start=schedule.week_start,
            week_end=schedule.week_end,
            status=schedule.status,
            created_by=schedule.created_by,
            notes=schedule.notes,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at,
            ai_optimization_score=schedule.ai_optimization_score,
            total_hours=schedule.total_hours,
            conflicts_count=schedule.conflicts_count
        )
        for schedule in schedules
    ]

@router.get("/{schedule_id}", response_model=ScheduleWithShifts)
async def get_schedule(
    schedule_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    schedule = await ScheduleService.get_schedule_with_shifts(schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    return schedule

@router.get("/employee/{employee_id}", response_model=List[Shift])
async def get_employee_schedule(
    employee_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    shifts = await ScheduleService.get_employee_shifts(employee_id)
    return [
        Shift(
            id=str(shift.id),
            employee_id=shift.employee_id,
            schedule_id=shift.schedule_id,
            date=shift.date,
            start_time=shift.start_time,
            end_time=shift.end_time,
            position=shift.position,
            location=shift.location,
            break_duration=shift.break_duration,
            status=shift.status,
            notes=shift.notes,
            created_at=shift.created_at,
            updated_at=shift.updated_at
        )
        for shift in shifts
    ]

@router.put("/{schedule_id}/publish")
async def publish_schedule(
    schedule_id: str,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    success = await ScheduleService.publish_schedule(schedule_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    return {"success": True, "message": "Schedule published successfully"}

@router.get("/{schedule_id}/export")
async def export_schedule(
    schedule_id: str,
    format: str = "json",
    current_user: UserInDB = Depends(get_current_admin_user)
):
    if format not in ["json", "csv"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid export format. Use 'json' or 'csv'"
        )
    
    export_data = await ScheduleService.export_schedule(schedule_id, format)
    if not export_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    return export_data
