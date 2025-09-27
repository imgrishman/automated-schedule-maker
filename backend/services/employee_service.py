from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from database.connection import get_database
from models.employee import EmployeeCreate, EmployeeUpdate, EmployeeInDB, EmployeeWithUser
from models.user import UserInDB

class EmployeeService:
    @staticmethod
    async def create_employee(employee_data: EmployeeCreate) -> EmployeeInDB:
        db = get_database()
        
        # Check if employee already exists
        existing_employee = await db.employees.find_one({"user_id": employee_data.user_id})
        if existing_employee:
            raise ValueError("Employee profile already exists for this user")
        
        # Create employee document
        employee_dict = employee_data.dict()
        employee_dict["created_at"] = datetime.utcnow()
        employee_dict["updated_at"] = datetime.utcnow()
        
        # Insert employee
        result = await db.employees.insert_one(employee_dict)
        employee_dict["_id"] = result.inserted_id
        
        return EmployeeInDB(**employee_dict)
    
    @staticmethod
    async def get_employee_by_id(employee_id: str) -> Optional[EmployeeInDB]:
        db = get_database()
        employee = await db.employees.find_one({"_id": ObjectId(employee_id)})
        if employee:
            return EmployeeInDB(**employee)
        return None
    
    @staticmethod
    async def get_employee_by_user_id(user_id: str) -> Optional[EmployeeInDB]:
        db = get_database()
        employee = await db.employees.find_one({"user_id": user_id})
        if employee:
            return EmployeeInDB(**employee)
        return None
    
    @staticmethod
    async def get_all_employees() -> List[EmployeeWithUser]:
        db = get_database()
        
        # Aggregate employees with user data
        pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$unwind": "$user"
            },
            {
                "$project": {
                    "_id": 1,
                    "user_id": 1,
                    "employee_id": 1,
                    "department": 1,
                    "position": 1,
                    "contract_type": 1,
                    "max_hours_per_week": 1,
                    "hourly_rate": 1,
                    "skills": 1,
                    "phone": 1,
                    "hire_date": 1,
                    "status": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "first_name": "$user.first_name",
                    "last_name": "$user.last_name",
                    "email": "$user.email"
                }
            }
        ]
        
        employees = []
        async for employee in db.employees.aggregate(pipeline):
            employee["id"] = str(employee["_id"])
            del employee["_id"]
            employees.append(EmployeeWithUser(**employee))
        
        return employees
    
    @staticmethod
    async def update_employee(employee_id: str, employee_data: EmployeeUpdate) -> Optional[EmployeeInDB]:
        db = get_database()
        
        update_data = {k: v for k, v in employee_data.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.employees.update_one(
            {"_id": ObjectId(employee_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            updated_employee = await db.employees.find_one({"_id": ObjectId(employee_id)})
            return EmployeeInDB(**updated_employee)
        
        return None
    
    @staticmethod
    async def delete_employee(employee_id: str) -> bool:
        db = get_database()
        result = await db.employees.delete_one({"_id": ObjectId(employee_id)})
        return result.deleted_count > 0
    
    @staticmethod
    async def get_employees_by_department(department: str) -> List[EmployeeWithUser]:
        db = get_database()
        
        pipeline = [
            {"$match": {"department": department}},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {"$unwind": "$user"},
            {
                "$project": {
                    "_id": 1,
                    "user_id": 1,
                    "employee_id": 1,
                    "department": 1,
                    "position": 1,
                    "contract_type": 1,
                    "max_hours_per_week": 1,
                    "hourly_rate": 1,
                    "skills": 1,
                    "phone": 1,
                    "hire_date": 1,
                    "status": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "first_name": "$user.first_name",
                    "last_name": "$user.last_name",
                    "email": "$user.email"
                }
            }
        ]
        
        employees = []
        async for employee in db.employees.aggregate(pipeline):
            employee["id"] = str(employee["_id"])
            del employee["_id"]
            employees.append(EmployeeWithUser(**employee))
        
        return employees
