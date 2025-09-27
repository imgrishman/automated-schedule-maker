import random
from typing import List, Dict, Tuple
from datetime import datetime, date, timedelta
from collections import defaultdict
import math

from models.employee import EmployeeWithUser
from models.availability import Availability, DayAvailability
from models.schedule import ScheduleGenerationRequest, Shift, ShiftCreate

class AIScheduler:
    def __init__(self):
        self.fairness_weight = 0.3
        self.coverage_weight = 0.4
        self.preference_weight = 0.3
    
    async def generate_optimal_schedule(
        self, 
        employees: List[EmployeeWithUser], 
        availabilities: List[Availability],
        request: ScheduleGenerationRequest
    ) -> Tuple[List[ShiftCreate], Dict]:
        """
        Generate an optimal schedule using AI algorithms
        """
        # Create availability lookup
        availability_map = {avail.employee_id: avail for avail in availabilities}
        
        # Generate shifts for the week
        shifts = []
        week_dates = self._get_week_dates(request.week_start)
        
        # Track employee hours for fairness
        employee_hours = defaultdict(int)
        
        # Generate shifts for each day
        for day_date in week_dates:
            day_name = day_date.strftime('%A').lower()
            daily_shifts = self._generate_daily_shifts(
                employees, availability_map, day_date, day_name, 
                request, employee_hours
            )
            shifts.extend(daily_shifts)
        
        # Calculate optimization metrics
        metrics = self._calculate_optimization_metrics(
            shifts, employees, availability_map, request
        )
        
        return shifts, metrics
    
    def _get_week_dates(self, week_start: date) -> List[date]:
        """Get all dates in the week"""
        dates = []
        for i in range(7):
            dates.append(week_start + timedelta(days=i))
        return dates
    
    def _generate_daily_shifts(
        self, 
        employees: List[EmployeeWithUser], 
        availability_map: Dict[str, Availability],
        day_date: date,
        day_name: str,
        request: ScheduleGenerationRequest,
        employee_hours: Dict[str, int]
    ) -> List[ShiftCreate]:
        """Generate shifts for a specific day"""
        shifts = []
        
        # Define shift slots (can be made configurable)
        shift_slots = [
            ("09:00", "17:00", "Morning Shift"),
            ("10:00", "18:00", "Day Shift"),
            ("12:00", "20:00", "Evening Shift"),
            ("14:00", "22:00", "Late Shift")
        ]
        
        # Filter available employees for this day
        available_employees = self._get_available_employees(
            employees, availability_map, day_name
        )
        
        # Assign shifts based on availability and fairness
        for start_time, end_time, shift_name in shift_slots:
            if not available_employees:
                break
                
            # Select best employee for this shift
            selected_employee = self._select_best_employee(
                available_employees, availability_map, day_name, 
                start_time, end_time, employee_hours, request
            )
            
            if selected_employee:
                shift_hours = self._calculate_shift_hours(start_time, end_time)
                
                # Check if employee can work these hours
                if (employee_hours[selected_employee.id] + shift_hours <= 
                    selected_employee.max_hours_per_week):
                    
                    shift = ShiftCreate(
                        employee_id=selected_employee.id,
                        date=day_date,
                        start_time=start_time,
                        end_time=end_time,
                        position=selected_employee.position,
                        location=selected_employee.department
                    )
                    shifts.append(shift)
                    employee_hours[selected_employee.id] += shift_hours
                    
                    # Remove employee from available list to avoid double booking
                    available_employees.remove(selected_employee)
        
        return shifts
    
    def _get_available_employees(
        self, 
        employees: List[EmployeeWithUser], 
        availability_map: Dict[str, Availability],
        day_name: str
    ) -> List[EmployeeWithUser]:
        """Get employees available for a specific day"""
        available = []
        
        for employee in employees:
            if employee.status.value != "active":
                continue
                
            availability = availability_map.get(employee.id)
            if not availability:
                continue
                
            day_availability = getattr(availability.weekly_availability, day_name)
            if day_availability.available:
                available.append(employee)
        
        return available
    
    def _select_best_employee(
        self,
        available_employees: List[EmployeeWithUser],
        availability_map: Dict[str, Availability],
        day_name: str,
        start_time: str,
        end_time: str,
        employee_hours: Dict[str, int],
        request: ScheduleGenerationRequest
    ) -> EmployeeWithUser:
        """Select the best employee for a shift using AI scoring"""
        if not available_employees:
            return None
        
        best_employee = None
        best_score = -1
        
        for employee in available_employees:
            score = self._calculate_employee_score(
                employee, availability_map, day_name, start_time, 
                end_time, employee_hours, request
            )
            
            if score > best_score:
                best_score = score
                best_employee = employee
        
        return best_employee
    
    def _calculate_employee_score(
        self,
        employee: EmployeeWithUser,
        availability_map: Dict[str, Availability],
        day_name: str,
        start_time: str,
        end_time: str,
        employee_hours: Dict[str, int],
        request: ScheduleGenerationRequest
    ) -> float:
        """Calculate AI score for employee assignment"""
        score = 0.0
        
        # Availability score (0-1)
        availability = availability_map.get(employee.id)
        if availability:
            day_availability = getattr(availability.weekly_availability, day_name)
            if self._time_fits_availability(start_time, end_time, day_availability):
                score += 1.0 * self.preference_weight
        
        # Fairness score (0-1) - prefer employees with fewer hours
        current_hours = employee_hours.get(employee.id, 0)
        max_hours = min(employee.max_hours_per_week, request.max_hours_per_employee)
        fairness_score = 1.0 - (current_hours / max_hours) if max_hours > 0 else 0
        score += fairness_score * self.fairness_weight
        
        # Coverage score (0-1) - always 1 if employee is available
        score += 1.0 * self.coverage_weight
        
        # Add some randomness to avoid always picking the same employee
        score += random.uniform(0, 0.1)
        
        return score
    
    def _time_fits_availability(
        self, 
        start_time: str, 
        end_time: str, 
        day_availability: DayAvailability
    ) -> bool:
        """Check if shift time fits within employee availability"""
        if not day_availability.available:
            return False
        
        if not day_availability.start_time or not day_availability.end_time:
            return True  # No specific time constraints
        
        # Convert times to minutes for comparison
        shift_start = self._time_to_minutes(start_time)
        shift_end = self._time_to_minutes(end_time)
        avail_start = self._time_to_minutes(day_availability.start_time)
        avail_end = self._time_to_minutes(day_availability.end_time)
        
        return shift_start >= avail_start and shift_end <= avail_end
    
    def _time_to_minutes(self, time_str: str) -> int:
        """Convert time string to minutes since midnight"""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    def _calculate_shift_hours(self, start_time: str, end_time: str) -> int:
        """Calculate shift duration in hours"""
        start_minutes = self._time_to_minutes(start_time)
        end_minutes = self._time_to_minutes(end_time)
        return (end_minutes - start_minutes) // 60
    
    def _calculate_optimization_metrics(
        self,
        shifts: List[ShiftCreate],
        employees: List[EmployeeWithUser],
        availability_map: Dict[str, Availability],
        request: ScheduleGenerationRequest
    ) -> Dict:
        """Calculate optimization metrics for the generated schedule"""
        total_shifts = len(shifts)
        total_hours = sum(self._calculate_shift_hours(s.start_time, s.end_time) for s in shifts)
        
        # Calculate fairness index (Gini coefficient)
        employee_hours = defaultdict(int)
        for shift in shifts:
            hours = self._calculate_shift_hours(shift.start_time, shift.end_time)
            employee_hours[shift.employee_id] += hours
        
        fairness_index = self._calculate_fairness_index(list(employee_hours.values()))
        
        # Calculate coverage percentage
        required_shifts = 7 * 4  # 7 days * 4 shifts per day (example)
        coverage_percentage = min(100, (total_shifts / required_shifts) * 100)
        
        # Calculate optimization score
        optimization_score = (
            fairness_index * self.fairness_weight +
            (coverage_percentage / 100) * self.coverage_weight +
            0.9 * self.preference_weight  # Assume 90% preference satisfaction
        ) * 100
        
        return {
            "optimization_score": round(optimization_score, 1),
            "fairness_index": round(fairness_index, 3),
            "coverage_percentage": round(coverage_percentage, 1),
            "total_shifts": total_shifts,
            "total_hours": total_hours,
            "conflicts_count": 0,  # Would be calculated based on actual conflicts
            "employee_distribution": dict(employee_hours)
        }
    
    def _calculate_fairness_index(self, hours_list: List[int]) -> float:
        """Calculate Gini coefficient for fairness measurement"""
        if not hours_list:
            return 1.0
        
        n = len(hours_list)
        if n == 1:
            return 1.0
        
        hours_list.sort()
        cumsum = sum((i + 1) * hours for i, hours in enumerate(hours_list))
        total_hours = sum(hours_list)
        
        if total_hours == 0:
            return 1.0
        
        gini = (2 * cumsum) / (n * total_hours) - (n + 1) / n
        return 1 - gini  # Convert to fairness index (higher is better)
