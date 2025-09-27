from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, time
from enum import Enum
from bson import ObjectId

class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"

class ContractType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"

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

class EmployeeBase(BaseModel):
    user_id: str
    employee_id: str
    department: str
    position: str
    contract_type: ContractType
    max_hours_per_week: int = 40
    hourly_rate: Optional[float] = None
    skills: List[str] = []
    phone: Optional[str] = None
    emergency_contact: Optional[Dict] = None
    hire_date: datetime
    status: EmployeeStatus = EmployeeStatus.ACTIVE

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    department: Optional[str] = None
    position: Optional[str] = None
    contract_type: Optional[ContractType] = None
    max_hours_per_week: Optional[int] = None
    hourly_rate: Optional[float] = None
    skills: Optional[List[str]] = None
    phone: Optional[str] = None
    emergency_contact: Optional[Dict] = None
    status: Optional[EmployeeStatus] = None

class EmployeeInDB(EmployeeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Employee(EmployeeBase):
    id: str
    created_at: datetime
    updated_at: datetime

class EmployeeWithUser(BaseModel):
    id: str
    user_id: str
    employee_id: str
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    contract_type: ContractType
    max_hours_per_week: int
    hourly_rate: Optional[float]
    skills: List[str]
    phone: Optional[str]
    hire_date: datetime
    status: EmployeeStatus
    created_at: datetime
    updated_at: datetime
