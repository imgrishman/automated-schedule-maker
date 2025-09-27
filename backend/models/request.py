from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum
from bson import ObjectId

class RequestType(str, Enum):
    TIME_OFF = "time_off"
    SHIFT_SWAP = "shift_swap"
    SCHEDULE_CHANGE = "schedule_change"
    OVERTIME = "overtime"

class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

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

class RequestBase(BaseModel):
    employee_id: str
    request_type: RequestType
    start_date: date
    end_date: Optional[date] = None
    reason: str
    status: RequestStatus = RequestStatus.PENDING
    notes: Optional[str] = None

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    status: Optional[RequestStatus] = None
    admin_notes: Optional[str] = None

class RequestInDB(RequestBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    admin_notes: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, date: str}

class Request(RequestBase):
    id: str
    created_at: datetime
    updated_at: datetime
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    admin_notes: Optional[str] = None
