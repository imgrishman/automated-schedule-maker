from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, List
from datetime import datetime, timedelta

from models.user import UserInDB
from services.analytics_service import AnalyticsService
from middleware.auth import get_current_admin_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_analytics(
    current_user: UserInDB = Depends(get_current_admin_user)
) -> Dict:
    try:
        analytics = await AnalyticsService.get_dashboard_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/employee-satisfaction")
async def get_employee_satisfaction(
    current_user: UserInDB = Depends(get_current_admin_user)
) -> List[Dict]:
    try:
        satisfaction_data = await AnalyticsService.get_employee_satisfaction_metrics()
        return satisfaction_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/schedule-efficiency")
async def get_schedule_efficiency(
    days: int = 30,
    current_user: UserInDB = Depends(get_current_admin_user)
) -> Dict:
    try:
        efficiency_data = await AnalyticsService.get_schedule_efficiency_trends(days)
        return efficiency_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/department-hours")
async def get_department_hours(
    current_user: UserInDB = Depends(get_current_admin_user)
) -> List[Dict]:
    try:
        department_data = await AnalyticsService.get_department_hours_distribution()
        return department_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/ai-insights")
async def get_ai_insights(
    current_user: UserInDB = Depends(get_current_admin_user)
) -> List[Dict]:
    try:
        insights = await AnalyticsService.get_ai_insights()
        return insights
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
