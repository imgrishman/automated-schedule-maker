from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId

from database.connection import get_database
from models.user import UserCreate, UserInDB, UserLogin, User
from middleware.auth import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
        db = get_database()
        user = await db.users.find_one({"email": email})
        if not user:
            return None
        if not AuthService.verify_password(password, user["hashed_password"]):
            return None
        return UserInDB(**user)
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> UserInDB:
        db = get_database()
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password
        hashed_password = AuthService.get_password_hash(user_data.password)
        
        # Create user document
        user_dict = user_data.dict(exclude={"password"})
        user_dict["hashed_password"] = hashed_password
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        
        # Insert user
        result = await db.users.insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        
        return UserInDB(**user_dict)
    
    @staticmethod
    async def login_user(login_data: UserLogin) -> dict:
        user = await AuthService.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise ValueError("Invalid credentials")
        
        # Update last login
        db = get_database()
        await db.users.update_one(
            {"_id": user.id},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        # Convert user to response format
        user_response = User(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            status=user.status,
            employee_id=user.employee_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800,  # 30 minutes
            "user": user_response
        }
