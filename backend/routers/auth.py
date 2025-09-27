from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from models.user import UserCreate, UserLogin, Token
from services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    try:
        user = await AuthService.create_user(user_data)
        return {
            "success": True,
            "message": "User created successfully",
            "user_id": str(user.id)
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    try:
        result = await AuthService.login_user(login_data)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/demo-login")
async def demo_login(demo_type: str):
    """Demo login endpoint for testing"""
    demo_credentials = {
        "admin": {"email": "admin@asp.com", "password": "admin123"},
        "employee": {"email": "employee@asp.com", "password": "employee123"}
    }
    
    if demo_type not in demo_credentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid demo type"
        )
    
    try:
        login_data = UserLogin(**demo_credentials[demo_type])
        result = await AuthService.login_user(login_data)
        return result
    except ValueError:
        # Create demo user if doesn't exist
        from models.user import UserRole
        user_data = UserCreate(
            email=demo_credentials[demo_type]["email"],
            password=demo_credentials[demo_type]["password"],
            first_name="Demo",
            last_name="User",
            role=UserRole.ADMIN if demo_type == "admin" else UserRole.EMPLOYEE
        )
        
        try:
            await AuthService.create_user(user_data)
            login_data = UserLogin(**demo_credentials[demo_type])
            result = await AuthService.login_user(login_data)
            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create demo user"
            )
