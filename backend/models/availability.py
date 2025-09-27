from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime, time
from bson import ObjectId

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

class DayAvailability(BaseModel):
    available: bool = False
    start_time: Optional[str] = None  # Format: "HH:MM"
    end_time: Optional[str] = None    # Format: "HH:MM"

class WeeklyAvailability(BaseModel):
    monday: DayAvailability = DayAvailability()
    tuesday: DayAvailability = DayAvailability()
    wednesday: DayAvailability = DayAvailability()
    thursday: DayAvailability = DayAvailability()
    friday: DayAvailability = DayAvailability()
    saturday: DayAvailability = DayAvailability()
    sunday: DayAvailability = DayAvailability()

class AvailabilityBase(BaseModel):
    employee_id: str
    weekly_availability: WeeklyAvailability
    max_hours_per_week: int = 40
    preferred_shift_length: int = 8  # hours
    notes: Optional[str] = None
    effective_date: datetime = Field(default_factory=datetime.utcnow)

class AvailabilityCreate(AvailabilityBase):
    pass

class AvailabilityUpdate(BaseModel):
    weekly_availability: Optional[WeeklyAvailability] = None
    max_hours_per_week: Optional[int] = None
    preferred_shift_length: Optional[int] = None
    notes: Optional[str] = None

class AvailabilityInDB(AvailabilityBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Availability(AvailabilityBase):
    id: str
    created_at: datetime
    updated_at: datetime
