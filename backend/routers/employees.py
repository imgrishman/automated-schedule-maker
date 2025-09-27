from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from models.employee import EmployeeCreate, EmployeeUpdate, Employee, EmployeeWithUser
from models.user import UserInDB
from services.employee_service import EmployeeService
from middleware.auth import get_current_admin_user, get_current_user

router = APIRouter()

@router.post("/", response_model=Employee)
async def create_employee(
    employee_data: EmployeeCreate,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    try:
        employee = await EmployeeService.create_employee(employee_data)
        return Employee(
            id=str(employee.id),
            user_id=employee.user_id,
            employee_id=employee.employee_id,
            department=employee.department,
            position=employee.position,
            contract_type=employee.contract_type,
            max_hours_per_week=employee.max_hours_per_week,
            hourly_rate=employee.hourly_rate,
            skills=employee.skills,
            phone=employee.phone,
            emergency_contact=employee.emergency_contact,
            hire_date=employee.hire_date,
            status=employee.status,
            created_at=employee.created_at,
            updated_at=employee.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[EmployeeWithUser])
async def get_all_employees(
    current_user: UserInDB = Depends(get_current_admin_user)
):
    employees = await EmployeeService.get_all_employees()
    return employees

@router.get("/me", response_model=Employee)
async def get_my_profile(
    current_user: UserInDB = Depends(get_current_user)
):
    employee = await EmployeeService.get_employee_by_user_id(str(current_user.id))
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee profile not found"
        )
    
    return Employee(
        id=str(employee.id),
        user_id=employee.user_id,
        employee_id=employee.employee_id,
        department=employee.department,
        position=employee.position,
        contract_type=employee.contract_type,
        max_hours_per_week=employee.max_hours_per_week,
        hourly_rate=employee.hourly_rate,
        skills=employee.skills,
        phone=employee.phone,
        emergency_contact=employee.emergency_contact,
        hire_date=employee.hire_date,
        status=employee.status,
        created_at=employee.created_at,
        updated_at=employee.updated_at
    )

@router.get("/{employee_id}", response_model=Employee)
async def get_employee(
    employee_id: str,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    employee = await EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return Employee(
        id=str(employee.id),
        user_id=employee.user_id,
        employee_id=employee.employee_id,
        department=employee.department,
        position=employee.position,
        contract_type=employee.contract_type,
        max_hours_per_week=employee.max_hours_per_week,
        hourly_rate=employee.hourly_rate,
        skills=employee.skills,
        phone=employee.phone,
        emergency_contact=employee.emergency_contact,
        hire_date=employee.hire_date,
        status=employee.status,
        created_at=employee.created_at,
        updated_at=employee.updated_at
    )

@router.put("/{employee_id}", response_model=Employee)
async def update_employee(
    employee_id: str,
    employee_data: EmployeeUpdate,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    employee = await EmployeeService.update_employee(employee_id, employee_data)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return Employee(
        id=str(employee.id),
        user_id=employee.user_id,
        employee_id=employee.employee_id,
        department=employee.department,
        position=employee.position,
        contract_type=employee.contract_type,
        max_hours_per_week=employee.max_hours_per_week,
        hourly_rate=employee.hourly_rate,
        skills=employee.skills,
        phone=employee.phone,
        emergency_contact=employee.emergency_contact,
        hire_date=employee.hire_date,
        status=employee.status,
        created_at=employee.created_at,
        updated_at=employee.updated_at
    )

@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: str,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    success = await EmployeeService.delete_employee(employee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return {"success": True, "message": "Employee deleted successfully"}

@router.get("/department/{department}", response_model=List[EmployeeWithUser])
async def get_employees_by_department(
    department: str,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    employees = await EmployeeService.get_employees_by_department(department)
    return employees
