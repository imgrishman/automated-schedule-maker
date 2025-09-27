from typing import List, Optional, Dict
from bson import ObjectId
from datetime import datetime, date, timedelta
import asyncio
import csv
import io

from database.connection import get_database
from models.schedule import (
    ScheduleCreate, ScheduleUpdate, ScheduleInDB, ScheduleWithShifts,
    ScheduleGenerationRequest, ShiftCreate, ShiftInDB, Shift, ScheduleStatus
)
from services.employee_service import EmployeeService
from services.availability_service import AvailabilityService
from services.ai_scheduler import AIScheduler

class ScheduleService:
    @staticmethod
    async def start_schedule_generation(request: ScheduleGenerationRequest, created_by: str) -> str:
        db = get_database()
        
        # Create schedule record
        schedule_data = ScheduleCreate(
            name=f"Schedule for {request.week_start}",
            week_start=request.week_start,
            week_end=request.week_start + timedelta(days=6),
            status=ScheduleStatus.GENERATING,
            created_by=created_by,
            notes="AI-generated schedule"
        )
        
        schedule_dict = schedule_data.dict()
        schedule_dict["created_at"] = datetime.utcnow()
        schedule_dict["updated_at"] = datetime.utcnow()
        
        result = await db.schedules.insert_one(schedule_dict)
        schedule_id = str(result.inserted_id)
        
        # Start background generation
        asyncio.create_task(ScheduleService._generate_schedule_background(schedule_id, request))
        
        return schedule_id
    
    @staticmethod
    async def _generate_schedule_background(schedule_id: str, request: ScheduleGenerationRequest):
        try:
            db = get_database()
            
            # Get employees and availability
            employees = await EmployeeService.get_all_employees()
            availabilities = await AvailabilityService.get_all_availability()
            
            # Generate schedule using AI
            ai_scheduler = AIScheduler()
            shifts, metrics = await ai_scheduler.generate_optimal_schedule(
                employees, availabilities, request
            )
            
            # Save shifts to database
            shift_docs = []
            for shift in shifts:
                shift_dict = shift.dict()
                shift_dict["schedule_id"] = schedule_id
                shift_dict["created_at"] = datetime.utcnow()
                shift_dict["updated_at"] = datetime.utcnow()
                shift_docs.append(shift_dict)
            
            if shift_docs:
                await db.shifts.insert_many(shift_docs)
            
            # Update schedule with metrics
            await db.schedules.update_one(
                {"_id": ObjectId(schedule_id)},
                {
                    "$set": {
                        "status": ScheduleStatus.DRAFT,
                        "ai_optimization_score": metrics["optimization_score"],
                        "total_hours": metrics["total_hours"],
                        "conflicts_count": metrics["conflicts_count"],
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
        except Exception as e:
            # Update schedule status to error
            await db.schedules.update_one(
                {"_id": ObjectId(schedule_id)},
                {
                    "$set": {
                        "status": ScheduleStatus.DRAFT,
                        "notes": f"Generation failed: {str(e)}",
                        "updated_at": datetime.utcnow()
                    }
                }
            )
    
    @staticmethod
    async def get_all_schedules() -> List[ScheduleInDB]:
        db = get_database()
        schedules = []
        
        async for schedule in db.schedules.find().sort("created_at", -1):
            schedules.append(ScheduleInDB(**schedule))
        
        return schedules
    
    @staticmethod
    async def get_schedule_with_shifts(schedule_id: str) -> Optional[ScheduleWithShifts]:
        db = get_database()
        
        # Get schedule
        schedule = await db.schedules.find_one({"_id": ObjectId(schedule_id)})
        if not schedule:
            return None
        
        # Get shifts
        shifts = []
        async for shift in db.shifts.find({"schedule_id": schedule_id}):
            shifts.append(Shift(
                id=str(shift["_id"]),
                employee_id=shift["employee_id"],
                schedule_id=shift["schedule_id"],
                date=shift["date"],
                start_time=shift["start_time"],
                end_time=shift["end_time"],
                position=shift["position"],
                location=shift.get("location"),
                break_duration=shift.get("break_duration", 30),
                status=shift.get("status", "scheduled"),
                notes=shift.get("notes"),
                created_at=shift["created_at"],
                updated_at=shift["updated_at"]
            ))
        
        return ScheduleWithShifts(
            id=str(schedule["_id"]),
            name=schedule["name"],
            week_start=schedule["week_start"],
            week_end=schedule["week_end"],
            status=schedule["status"],
            created_by=schedule["created_by"],
            notes=schedule.get("notes"),
            created_at=schedule["created_at"],
            updated_at=schedule["updated_at"],
            ai_optimization_score=schedule.get("ai_optimization_score"),
            total_hours=schedule.get("total_hours"),
            conflicts_count=schedule.get("conflicts_count", 0),
            shifts=shifts
        )
    
    @staticmethod
    async def get_employee_shifts(employee_id: str) -> List[ShiftInDB]:
        db = get_database()
        shifts = []
        
        # Get current and upcoming shifts
        current_date = datetime.utcnow().date()
        async for shift in db.shifts.find({
            "employee_id": employee_id,
            "date": {"$gte": current_date}
        }).sort("date", 1):
            shifts.append(ShiftInDB(**shift))
        
        return shifts
    
    @staticmethod
    async def publish_schedule(schedule_id: str) -> bool:
        db = get_database()
        
        result = await db.schedules.update_one(
            {"_id": ObjectId(schedule_id)},
            {
                "$set": {
                    "status": ScheduleStatus.PUBLISHED,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    @staticmethod
    async def export_schedule(schedule_id: str, format: str) -> Optional[Dict]:
        schedule = await ScheduleService.get_schedule_with_shifts(schedule_id)
        if not schedule:
            return None
        
        if format == "json":
            return {
                "schedule": schedule.dict(),
                "export_date": datetime.utcnow().isoformat()
            }
        
        elif format == "csv":
            # Create CSV data
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                "Employee ID", "Date", "Start Time", "End Time", 
                "Position", "Location", "Status", "Notes"
            ])
            
            # Write shifts
            for shift in schedule.shifts:
                writer.writerow([
                    shift.employee_id,
                    shift.date,
                    shift.start_time,
                    shift.end_time,
                    shift.position,
                    shift.location or "",
                    shift.status,
                    shift.notes or ""
                ])
            
            return {
                "csv_data": output.getvalue(),
                "filename": f"schedule_{schedule_id}.csv"
            }
        
        return None
