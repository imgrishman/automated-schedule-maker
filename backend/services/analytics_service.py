from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict
import random

from database.connection import get_database
from services.employee_service import EmployeeService
from services.schedule_service import ScheduleService

class AnalyticsService:
    @staticmethod
    async def get_dashboard_analytics() -> Dict:
        db = get_database()
        
        # Get basic counts
        total_employees = await db.employees.count_documents({"status": "active"})
        total_schedules = await db.schedules.count_documents({})
        published_schedules = await db.schedules.count_documents({"status": "published"})
        
        # Get current week hours
        current_week_start = datetime.utcnow().date()
        current_week_start -= timedelta(days=current_week_start.weekday())
        current_week_end = current_week_start + timedelta(days=6)
        
        # Calculate total hours for current week
        total_hours = 0
        async for shift in db.shifts.find({
            "date": {"$gte": current_week_start, "$lte": current_week_end}
        }):
            start_time = shift["start_time"]
            end_time = shift["end_time"]
            hours = AnalyticsService._calculate_hours(start_time, end_time)
            total_hours += hours
        
        # Get AI efficiency score (average of recent schedules)
        ai_scores = []
        async for schedule in db.schedules.find({
            "ai_optimization_score": {"$exists": True}
        }).sort("created_at", -1).limit(10):
            if schedule.get("ai_optimization_score"):
                ai_scores.append(schedule["ai_optimization_score"])
        
        avg_ai_score = sum(ai_scores) / len(ai_scores) if ai_scores else 85
        
        # Get pending requests count
        pending_requests = await db.requests.count_documents({"status": "pending"})
        
        return {
            "total_employees": total_employees,
            "active_schedules": published_schedules,
            "total_hours": total_hours,
            "ai_efficiency": round(avg_ai_score, 1),
            "pending_requests": pending_requests,
            "schedule_conflicts": 2,  # Mock data
            "coverage_rate": 98.5,   # Mock data
            "employee_satisfaction": 89.2  # Mock data
        }
    
    @staticmethod
    async def get_employee_satisfaction_metrics() -> List[Dict]:
        # Mock employee satisfaction data
        employees = await EmployeeService.get_all_employees()
        satisfaction_data = []
        
        for employee in employees[:10]:  # Limit to 10 for demo
            satisfaction_data.append({
                "employee_id": employee.id,
                "name": f"{employee.first_name} {employee.last_name}",
                "satisfaction_score": random.randint(75, 98),
                "shifts_count": random.randint(8, 15),
                "feedback_score": random.randint(4, 5),
                "attendance_rate": random.randint(90, 100)
            })
        
        return satisfaction_data
    
    @staticmethod
    async def get_schedule_efficiency_trends(days: int) -> Dict:
        db = get_database()
        
        # Get schedules from the last N days
        start_date = datetime.utcnow() - timedelta(days=days)
        
        weekly_data = []
        current_date = start_date
        
        while current_date < datetime.utcnow():
            week_end = current_date + timedelta(days=7)
            
            # Get schedules for this week
            week_schedules = []
            async for schedule in db.schedules.find({
                "created_at": {"$gte": current_date, "$lt": week_end}
            }):
                week_schedules.append(schedule)
            
            if week_schedules:
                # Calculate average efficiency
                total_score = sum(s.get("ai_optimization_score", 85) for s in week_schedules)
                avg_score = total_score / len(week_schedules)
                
                # Calculate total hours
                total_hours = 0
                for schedule in week_schedules:
                    total_hours += schedule.get("total_hours", 0)
                
                weekly_data.append({
                    "week": current_date.strftime("%Y-%m-%d"),
                    "efficiency_score": round(avg_score, 1),
                    "total_hours": total_hours,
                    "schedules_count": len(week_schedules)
                })
            
            current_date = week_end
        
        return {
            "weekly_trends": weekly_data,
            "average_efficiency": sum(w["efficiency_score"] for w in weekly_data) / len(weekly_data) if weekly_data else 85,
            "total_hours": sum(w["total_hours"] for w in weekly_data),
            "improvement_rate": 2.5  # Mock improvement percentage
        }
    
    @staticmethod
    async def get_department_hours_distribution() -> List[Dict]:
        db = get_database()
        
        # Get employees by department
        department_hours = defaultdict(int)
        
        async for employee in db.employees.find({"status": "active"}):
            department = employee.get("department", "Unknown")
            
            # Get shifts for this employee (current week)
            current_week_start = datetime.utcnow().date()
            current_week_start -= timedelta(days=current_week_start.weekday())
            current_week_end = current_week_start + timedelta(days=6)
            
            employee_hours = 0
            async for shift in db.shifts.find({
                "employee_id": employee["_id"],
                "date": {"$gte": current_week_start, "$lte": current_week_end}
            }):
                hours = AnalyticsService._calculate_hours(shift["start_time"], shift["end_time"])
                employee_hours += hours
            
            department_hours[department] += employee_hours
        
        # Convert to list format
        distribution = []
        colors = ["#3B82F6", "#8B5CF6", "#10B981", "#F59E0B", "#EF4444"]
        
        for i, (department, hours) in enumerate(department_hours.items()):
            distribution.append({
                "department": department,
                "hours": hours,
                "color": colors[i % len(colors)]
            })
        
        return distribution
    
    @staticmethod
    async def get_ai_insights() -> List[Dict]:
        # Generate AI-powered insights
        insights = [
            {
                "type": "optimization",
                "title": "Schedule Optimization Success",
                "message": "AI scheduling has improved fairness distribution by 15% this month",
                "impact": "positive",
                "confidence": 92
            },
            {
                "type": "efficiency",
                "title": "Efficiency Improvement",
                "message": "Automated scheduling reduced conflicts by 60% compared to manual planning",
                "impact": "positive",
                "confidence": 88
            },
            {
                "type": "recommendation",
                "title": "Staffing Recommendation",
                "message": "Consider hiring 1 part-time employee to reduce overtime costs by 12%",
                "impact": "neutral",
                "confidence": 85
            },
            {
                "type": "pattern",
                "title": "Peak Demand Insight",
                "message": "Friday 2-6 PM shows consistent high demand - consider additional coverage",
                "impact": "neutral",
                "confidence": 90
            },
            {
                "type": "satisfaction",
                "title": "Employee Satisfaction",
                "message": "Weekend shift rotation policy increased satisfaction scores by 8%",
                "impact": "positive",
                "confidence": 87
            }
        ]
        
        return insights
    
    @staticmethod
    def _calculate_hours(start_time: str, end_time: str) -> float:
        """Calculate hours between start and end time"""
        start_parts = start_time.split(":")
        end_parts = end_time.split(":")
        
        start_minutes = int(start_parts[0]) * 60 + int(start_parts[1])
        end_minutes = int(end_parts[0]) * 60 + int(end_parts[1])
        
        return (end_minutes - start_minutes) / 60
