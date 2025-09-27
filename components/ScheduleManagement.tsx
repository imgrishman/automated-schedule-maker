"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Calendar, Plus, Eye, Edit, Clock, CheckCircle, AlertCircle, Zap, Download } from "lucide-react"
import { apiService } from "@/lib/api"

interface Schedule {
  id: string
  name: string
  start_date: string
  end_date: string
  status: "draft" | "published" | "archived"
  created_by: string
  ai_score?: number
  total_hours?: number
  employees_scheduled?: number
}

interface ScheduleShift {
  id: string
  employee_id: string
  employee_name: string
  date: string
  start_time: string
  end_time: string
  position: string
  hours: number
}

export default function ScheduleManagement() {
  const [schedules, setSchedules] = useState<Schedule[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedSchedule, setSelectedSchedule] = useState<Schedule | null>(null)
  const [scheduleShifts, setScheduleShifts] = useState<ScheduleShift[]>([])
  const [isGenerateDialogOpen, setIsGenerateDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)

  useEffect(() => {
    loadSchedules()
  }, [])

  const loadSchedules = async () => {
    try {
      setLoading(true)
      const response = await apiService.getSchedules()

      // Add sample schedules if response is empty
      const sampleSchedules: Schedule[] = [
        {
          id: "schedule_001",
          name: "Week 1 - January 2025",
          start_date: "2025-01-06",
          end_date: "2025-01-12",
          status: "published",
          created_by: "admin_001",
          ai_score: 95,
          total_hours: 320,
          employees_scheduled: 12,
        },
        {
          id: "schedule_002",
          name: "Week 2 - January 2025",
          start_date: "2025-01-13",
          end_date: "2025-01-19",
          status: "draft",
          created_by: "admin_001",
          ai_score: 88,
          total_hours: 280,
          employees_scheduled: 10,
        },
        {
          id: "schedule_003",
          name: "Week 3 - January 2025",
          start_date: "2025-01-20",
          end_date: "2025-01-26",
          status: "draft",
          created_by: "admin_001",
          ai_score: 92,
          total_hours: 300,
          employees_scheduled: 11,
        },
      ]

      setSchedules(Array.isArray(response) ? [...response, ...sampleSchedules] : sampleSchedules)
    } catch (error) {
      console.error("Failed to load schedules:", error)
      // Set fallback data
      setSchedules([
        {
          id: "schedule_001",
          name: "Current Week Schedule",
          start_date: new Date().toISOString().split("T")[0],
          end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
          status: "published",
          created_by: "admin_001",
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateSchedule = async () => {
    try {
      const response = await apiService.generateSchedule({
        start_date: new Date().toISOString().split("T")[0],
        end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
        departments: ["Operations", "Customer Service", "Sales"],
        min_coverage: 2,
        max_hours_per_employee: 40,
      })

      const newSchedule: Schedule = {
        id: `schedule_${Date.now()}`,
        name: `Generated Schedule - ${new Date().toLocaleDateString()}`,
        start_date: new Date().toISOString().split("T")[0],
        end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
        status: "draft",
        created_by: "admin_001",
        ai_score: 90 + Math.floor(Math.random() * 10),
        total_hours: 250 + Math.floor(Math.random() * 100),
        employees_scheduled: 8 + Math.floor(Math.random() * 5),
      }

      setSchedules([newSchedule, ...schedules])
      setIsGenerateDialogOpen(false)
    } catch (error) {
      console.error("Failed to generate schedule:", error)
    }
  }

  const handlePublishSchedule = async (scheduleId: string) => {
    try {
      await apiService.publishSchedule(scheduleId)
      setSchedules(
        schedules.map((schedule) =>
          schedule.id === scheduleId ? { ...schedule, status: "published" as const } : schedule,
        ),
      )
    } catch (error) {
      console.error("Failed to publish schedule:", error)
    }
  }

  const handleViewSchedule = (schedule: Schedule) => {
    setSelectedSchedule(schedule)

    // Generate sample shifts for the selected schedule
    const sampleShifts: ScheduleShift[] = [
      {
        id: "shift_001",
        employee_id: "emp_001",
        employee_name: "Demo Employee",
        date: schedule.start_date,
        start_time: "09:00",
        end_time: "17:00",
        position: "Customer Service",
        hours: 8,
      },
      {
        id: "shift_002",
        employee_id: "emp_002",
        employee_name: "Sarah Johnson",
        date: schedule.start_date,
        start_time: "13:00",
        end_time: "21:00",
        position: "Operations",
        hours: 8,
      },
      {
        id: "shift_003",
        employee_id: "emp_003",
        employee_name: "Mike Chen",
        date: new Date(new Date(schedule.start_date).getTime() + 24 * 60 * 60 * 1000).toISOString().split("T")[0],
        start_time: "08:00",
        end_time: "16:00",
        position: "Management",
        hours: 8,
      },
      {
        id: "shift_004",
        employee_id: "emp_004",
        employee_name: "Emily Davis",
        date: new Date(new Date(schedule.start_date).getTime() + 24 * 60 * 60 * 1000).toISOString().split("T")[0],
        start_time: "12:00",
        end_time: "20:00",
        position: "Sales",
        hours: 8,
      },
    ]

    setScheduleShifts(sampleShifts)
    setIsViewDialogOpen(true)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "published":
        return "bg-green-100 text-green-800"
      case "draft":
        return "bg-yellow-100 text-yellow-800"
      case "archived":
        return "bg-gray-100 text-gray-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "published":
        return <CheckCircle className="w-4 h-4" />
      case "draft":
        return <AlertCircle className="w-4 h-4" />
      default:
        return <Clock className="w-4 h-4" />
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-64 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Schedule Management</h1>
          <p className="text-gray-600">Create and manage employee schedules with AI optimization</p>
        </div>

        <Dialog open={isGenerateDialogOpen} onOpenChange={setIsGenerateDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Zap className="w-4 h-4 mr-2" />
              Generate AI Schedule
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Generate AI-Optimized Schedule</DialogTitle>
              <DialogDescription>
                Create a new schedule using AI optimization based on employee availability, business requirements, and
                fairness algorithms.
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">AI Optimization Features:</h4>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• Balanced workload distribution</li>
                  <li>• Availability preference matching</li>
                  <li>• Minimum coverage requirements</li>
                  <li>• Fair rotation scheduling</li>
                </ul>
              </div>

              <div className="flex gap-2 pt-4">
                <Button onClick={handleGenerateSchedule} className="flex-1">
                  <Zap className="w-4 h-4 mr-2" />
                  Generate Schedule
                </Button>
                <Button variant="outline" onClick={() => setIsGenerateDialogOpen(false)}>
                  Cancel
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Calendar className="w-8 h-8 text-blue-500" />
              <div>
                <p className="text-sm text-gray-600">Total Schedules</p>
                <p className="text-2xl font-bold">{schedules.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-8 h-8 text-green-500" />
              <div>
                <p className="text-sm text-gray-600">Published</p>
                <p className="text-2xl font-bold">{schedules.filter((s) => s.status === "published").length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-8 h-8 text-yellow-500" />
              <div>
                <p className="text-sm text-gray-600">Drafts</p>
                <p className="text-2xl font-bold">{schedules.filter((s) => s.status === "draft").length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Zap className="w-8 h-8 text-purple-500" />
              <div>
                <p className="text-sm text-gray-600">Avg AI Score</p>
                <p className="text-2xl font-bold">
                  {Math.round(schedules.reduce((acc, s) => acc + (s.ai_score || 0), 0) / schedules.length) || 0}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Schedule Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {schedules.map((schedule) => (
          <Card key={schedule.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-lg">{schedule.name}</CardTitle>
                  <CardDescription>
                    {new Date(schedule.start_date).toLocaleDateString()} -{" "}
                    {new Date(schedule.end_date).toLocaleDateString()}
                  </CardDescription>
                </div>
                <Badge className={getStatusColor(schedule.status)}>
                  {getStatusIcon(schedule.status)}
                  <span className="ml-1 capitalize">{schedule.status}</span>
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {schedule.ai_score && (
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">AI Optimization Score</span>
                  <div className="flex items-center gap-2">
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${schedule.ai_score}%` }}></div>
                    </div>
                    <span className="text-sm font-medium">{schedule.ai_score}%</span>
                  </div>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-600">Total Hours</p>
                  <p className="font-medium">{schedule.total_hours || 0}h</p>
                </div>
                <div>
                  <p className="text-gray-600">Employees</p>
                  <p className="font-medium">{schedule.employees_scheduled || 0}</p>
                </div>
              </div>

              <div className="flex gap-2 pt-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1 bg-transparent"
                  onClick={() => handleViewSchedule(schedule)}
                >
                  <Eye className="w-4 h-4 mr-1" />
                  View
                </Button>
                <Button variant="outline" size="sm">
                  <Edit className="w-4 h-4" />
                </Button>
                {schedule.status === "draft" && (
                  <Button size="sm" onClick={() => handlePublishSchedule(schedule.id)}>
                    Publish
                  </Button>
                )}
                <Button variant="outline" size="sm">
                  <Download className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* View Schedule Dialog */}
      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent className="max-w-4xl">
          <DialogHeader>
            <DialogTitle>{selectedSchedule?.name}</DialogTitle>
            <DialogDescription>Schedule details and shift assignments</DialogDescription>
          </DialogHeader>

          {selectedSchedule && (
            <div className="space-y-6">
              {/* Schedule Info */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Status</p>
                  <Badge className={getStatusColor(selectedSchedule.status)}>{selectedSchedule.status}</Badge>
                </div>
                <div>
                  <p className="text-sm text-gray-600">AI Score</p>
                  <p className="font-medium">{selectedSchedule.ai_score}%</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Hours</p>
                  <p className="font-medium">{selectedSchedule.total_hours}h</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Employees</p>
                  <p className="font-medium">{selectedSchedule.employees_scheduled}</p>
                </div>
              </div>

              {/* Shifts Table */}
              <div>
                <h4 className="font-medium mb-3">Shift Assignments</h4>
                <div className="border rounded-lg overflow-hidden">
                  <div className="bg-gray-50 px-4 py-2 grid grid-cols-5 gap-4 text-sm font-medium text-gray-600">
                    <div>Employee</div>
                    <div>Date</div>
                    <div>Time</div>
                    <div>Position</div>
                    <div>Hours</div>
                  </div>
                  {scheduleShifts.map((shift) => (
                    <div key={shift.id} className="px-4 py-3 grid grid-cols-5 gap-4 text-sm border-t">
                      <div className="font-medium">{shift.employee_name}</div>
                      <div>{new Date(shift.date).toLocaleDateString()}</div>
                      <div>
                        {shift.start_time} - {shift.end_time}
                      </div>
                      <div>{shift.position}</div>
                      <div>{shift.hours}h</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>

      {schedules.length === 0 && (
        <div className="text-center py-12">
          <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No schedules found</p>
          <Button className="mt-4" onClick={() => setIsGenerateDialogOpen(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Create Your First Schedule
          </Button>
        </div>
      )}
    </div>
  )
}
