from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, date, time
from enum import Enum
from bson import ObjectId

class ScheduleStatus(str, Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class ShiftStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ShiftBase(BaseModel):
    employee_id: str
    date: date
    start_time: str  # Format: "HH:MM"
    end_time: str    # Format: "HH:MM"
    position: str
    location: Optional[str] = None
    break_duration: int = 30  # minutes
    status: ShiftStatus = ShiftStatus.SCHEDULED
    notes: Optional[str] = None

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(BaseModel):
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    break_duration: Optional[int] = None
    status: Optional[ShiftStatus] = None
    notes: Optional[str] = None

class ShiftInDB(ShiftBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    schedule_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, date: str}

class Shift(ShiftBase):
    id: str
    schedule_id: str
    created_at: datetime
    updated_at: datetime

class ScheduleBase(BaseModel):
    name: str
    week_start: date
    week_end: date
    status: ScheduleStatus = ScheduleStatus.DRAFT
    created_by: str
    notes: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[ScheduleStatus] = None
    notes: Optional[str] = None

class ScheduleInDB(ScheduleBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    ai_optimization_score: Optional[float] = None
    total_hours: Optional[float] = None
    conflicts_count: int = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, date: str}

class Schedule(ScheduleBase):
    id: str
    created_at: datetime
    updated_at: datetime
    ai_optimization_score: Optional[float] = None
    total_hours: Optional[float] = None
    conflicts_count: int = 0

class ScheduleWithShifts(Schedule):
    shifts: List[Shift] = []

class ScheduleGenerationRequest(BaseModel):
    week_start: date
    min_hours_per_employee: int = 20
    max_hours_per_employee: int = 40
    shift_length: int = 8
    priorities: Optional[str] = None
    department_requirements: Optional[Dict] = None
