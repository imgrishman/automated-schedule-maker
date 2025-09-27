from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from database.connection import get_database
from models.availability import AvailabilityCreate, AvailabilityUpdate, AvailabilityInDB

class AvailabilityService:
    @staticmethod
    async def create_availability(availability_data: AvailabilityCreate) -> AvailabilityInDB:
        db = get_database()
        
        # Create availability document
        availability_dict = availability_data.dict()
        availability_dict["created_at"] = datetime.utcnow()
        availability_dict["updated_at"] = datetime.utcnow()
        
        # Insert availability
        result = await db.availability.insert_one(availability_dict)
        availability_dict["_id"] = result.inserted_id
        
        return AvailabilityInDB(**availability_dict)
    
    @staticmethod
    async def get_current_availability(employee_id: str) -> Optional[AvailabilityInDB]:
        db = get_database()
        availability = await db.availability.find_one(
            {"employee_id": employee_id},
            sort=[("effective_date", -1)]
        )
        if availability:
            return AvailabilityInDB(**availability)
        return None
    
    @staticmethod
    async def get_all_availability() -> List[AvailabilityInDB]:
        db = get_database()
        availabilities = []
        
        # Get the most recent availability for each employee
        pipeline = [
            {"$sort": {"employee_id": 1, "effective_date": -1}},
            {"$group": {
                "_id": "$employee_id",
                "doc": {"$first": "$$ROOT"}
            }},
            {"$replaceRoot": {"newRoot": "$doc"}}
        ]
        
        async for availability in db.availability.aggregate(pipeline):
            availabilities.append(AvailabilityInDB(**availability))
        
        return availabilities
    
    @staticmethod
    async def update_availability(availability_id: str, availability_data: AvailabilityUpdate) -> Optional[AvailabilityInDB]:
        db = get_database()
        
        update_data = {k: v for k, v in availability_data.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.availability.update_one(
            {"_id": ObjectId(availability_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            updated_availability = await db.availability.find_one({"_id": ObjectId(availability_id)})
            return AvailabilityInDB(**updated_availability)
        
        return None
    
    @staticmethod
    async def delete_availability(availability_id: str) -> bool:
        db = get_database()
        result = await db.availability.delete_one({"_id": ObjectId(availability_id)})
        return result.deleted_count > 0
