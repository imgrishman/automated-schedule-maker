"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Clock, Users, CheckCircle, XCircle, Edit, Save, X } from "lucide-react"
import { apiService } from "@/lib/api"

interface AvailabilitySlot {
  id: string
  employee_id: string
  employee_name: string
  day_of_week: string
  start_time: string
  end_time: string
  available: boolean
  preferred?: boolean
}

interface Employee {
  id: string
  name: string
  department: string
  role: string
}

const DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

const TIME_SLOTS = [
  "06:00",
  "07:00",
  "08:00",
  "09:00",
  "10:00",
  "11:00",
  "12:00",
  "13:00",
  "14:00",
  "15:00",
  "16:00",
  "17:00",
  "18:00",
  "19:00",
  "20:00",
  "21:00",
  "22:00",
  "23:00",
]

export default function AvailabilityManagement() {
  const [availability, setAvailability] = useState<AvailabilitySlot[]>([])
  const [employees, setEmployees] = useState<Employee[]>([])
  const [selectedEmployee, setSelectedEmployee] = useState<string>("all")
  const [loading, setLoading] = useState(true)
  const [editMode, setEditMode] = useState(false)
  const [editingSlots, setEditingSlots] = useState<{ [key: string]: AvailabilitySlot }>({})

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)

      // Load employees and availability
      const [employeesResponse, availabilityResponse] = await Promise.all([
        apiService.getEmployees(),
        apiService.getAvailability(),
      ])

      // Sample employees data
      const sampleEmployees: Employee[] = [
        { id: "emp_001", name: "Demo Employee", department: "Operations", role: "employee" },
        { id: "emp_002", name: "Sarah Johnson", department: "Customer Service", role: "employee" },
        { id: "emp_003", name: "Mike Chen", department: "Operations", role: "manager" },
        { id: "emp_004", name: "Emily Davis", department: "Sales", role: "employee" },
        { id: "emp_005", name: "Alex Rodriguez", department: "Customer Service", role: "employee" },
      ]

      // Sample availability data
      const sampleAvailability: AvailabilitySlot[] = []

      sampleEmployees.forEach((employee) => {
        DAYS_OF_WEEK.forEach((day) => {
          // Generate realistic availability patterns
          const isWeekend = day === "Saturday" || day === "Sunday"
          const available = Math.random() > (isWeekend ? 0.6 : 0.2)

          if (available) {
            const startHour = 8 + Math.floor(Math.random() * 4) // 8-11 AM start
            const endHour = 16 + Math.floor(Math.random() * 5) // 4-8 PM end

            sampleAvailability.push({
              id: `avail_${employee.id}_${day.toLowerCase()}`,
              employee_id: employee.id,
              employee_name: employee.name,
              day_of_week: day.toLowerCase(),
              start_time: `${startHour.toString().padStart(2, "0")}:00`,
              end_time: `${endHour.toString().padStart(2, "0")}:00`,
              available: true,
              preferred: Math.random() > 0.7,
            })
          } else {
            sampleAvailability.push({
              id: `avail_${employee.id}_${day.toLowerCase()}`,
              employee_id: employee.id,
              employee_name: employee.name,
              day_of_week: day.toLowerCase(),
              start_time: "09:00",
              end_time: "17:00",
              available: false,
            })
          }
        })
      })

      setEmployees(sampleEmployees)
      setAvailability(sampleAvailability)
    } catch (error) {
      console.error("Failed to load data:", error)
      // Set fallback data
      setEmployees([{ id: "emp_001", name: "Demo Employee", department: "Operations", role: "employee" }])
      setAvailability([
        {
          id: "avail_001",
          employee_id: "emp_001",
          employee_name: "Demo Employee",
          day_of_week: "monday",
          start_time: "09:00",
          end_time: "17:00",
          available: true,
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleAvailabilityToggle = (slotId: string) => {
    if (!editMode) return

    const slot = availability.find((a) => a.id === slotId)
    if (!slot) return

    const updatedSlot = { ...slot, available: !slot.available }
    setEditingSlots((prev) => ({ ...prev, [slotId]: updatedSlot }))
  }

  const handleTimeChange = (slotId: string, field: "start_time" | "end_time", value: string) => {
    if (!editMode) return

    const slot = availability.find((a) => a.id === slotId) || editingSlots[slotId]
    if (!slot) return

    const updatedSlot = { ...slot, [field]: value }
    setEditingSlots((prev) => ({ ...prev, [slotId]: updatedSlot }))
  }

  const saveChanges = async () => {
    try {
      // Update availability with edited slots
      const updatedAvailability = availability.map((slot) => (editingSlots[slot.id] ? editingSlots[slot.id] : slot))

      setAvailability(updatedAvailability)
      setEditingSlots({})
      setEditMode(false)

      // In a real app, you would save to the backend here
      console.log("Saving availability changes:", editingSlots)
    } catch (error) {
      console.error("Failed to save changes:", error)
    }
  }

  const cancelEdit = () => {
    setEditingSlots({})
    setEditMode(false)
  }

  const filteredAvailability =
    selectedEmployee === "all" ? availability : availability.filter((a) => a.employee_id === selectedEmployee)

  const getAvailabilityForEmployeeAndDay = (employeeId: string, day: string) => {
    return availability.find((a) => a.employee_id === employeeId && a.day_of_week === day.toLowerCase())
  }

  const getDisplaySlot = (slotId: string) => {
    return editingSlots[slotId] || availability.find((a) => a.id === slotId)
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Availability Management</h1>
          <p className="text-gray-600">Manage employee availability and time preferences</p>
        </div>

        <div className="flex gap-2">
          {editMode ? (
            <>
              <Button onClick={saveChanges} size="sm">
                <Save className="w-4 h-4 mr-2" />
                Save Changes
              </Button>
              <Button variant="outline" onClick={cancelEdit} size="sm">
                <X className="w-4 h-4 mr-2" />
                Cancel
              </Button>
            </>
          ) : (
            <Button onClick={() => setEditMode(true)} size="sm">
              <Edit className="w-4 h-4 mr-2" />
              Edit Availability
            </Button>
          )}
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <Select value={selectedEmployee} onValueChange={setSelectedEmployee}>
          <SelectTrigger className="w-full sm:w-64">
            <SelectValue placeholder="Select Employee" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Employees</SelectItem>
            {employees.map((employee) => (
              <SelectItem key={employee.id} value={employee.id}>
                {employee.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Users className="w-8 h-8 text-blue-500" />
              <div>
                <p className="text-sm text-gray-600">Total Employees</p>
                <p className="text-2xl font-bold">{employees.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-8 h-8 text-green-500" />
              <div>
                <p className="text-sm text-gray-600">Available Slots</p>
                <p className="text-2xl font-bold">{availability.filter((a) => a.available).length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <XCircle className="w-8 h-8 text-red-500" />
              <div>
                <p className="text-sm text-gray-600">Unavailable</p>
                <p className="text-2xl font-bold">{availability.filter((a) => !a.available).length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Clock className="w-8 h-8 text-purple-500" />
              <div>
                <p className="text-sm text-gray-600">Avg Hours/Week</p>
                <p className="text-2xl font-bold">32</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Availability Grid */}
      <Card>
        <CardHeader>
          <CardTitle>Weekly Availability Grid</CardTitle>
          <CardDescription>
            {editMode ? "Click to toggle availability or adjust times" : "View employee availability across the week"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <div className="min-w-full">
              {/* Header */}
              <div className="grid grid-cols-8 gap-2 mb-4">
                <div className="font-medium text-gray-600 p-2">Employee</div>
                {DAYS_OF_WEEK.map((day) => (
                  <div key={day} className="font-medium text-gray-600 p-2 text-center">
                    {day.slice(0, 3)}
                  </div>
                ))}
              </div>

              {/* Employee Rows */}
              {(selectedEmployee === "all" ? employees : employees.filter((e) => e.id === selectedEmployee)).map(
                (employee) => (
                  <div key={employee.id} className="grid grid-cols-8 gap-2 mb-2 p-2 bg-gray-50 rounded-lg">
                    <div className="flex flex-col justify-center">
                      <div className="font-medium text-sm">{employee.name}</div>
                      <div className="text-xs text-gray-500">{employee.department}</div>
                    </div>

                    {DAYS_OF_WEEK.map((day) => {
                      const slot = getAvailabilityForEmployeeAndDay(employee.id, day)
                      const displaySlot = slot ? getDisplaySlot(slot.id) : null

                      return (
                        <div key={day} className="p-1">
                          {displaySlot ? (
                            <div
                              className={`p-2 rounded text-xs cursor-pointer transition-colors ${
                                displaySlot.available
                                  ? displaySlot.preferred
                                    ? "bg-green-200 text-green-800 border-2 border-green-400"
                                    : "bg-green-100 text-green-800"
                                  : "bg-red-100 text-red-800"
                              } ${editMode ? "hover:opacity-75" : ""}`}
                              onClick={() => editMode && handleAvailabilityToggle(displaySlot.id)}
                            >
                              {displaySlot.available ? (
                                <div className="space-y-1">
                                  {editMode ? (
                                    <>
                                      <Select
                                        value={displaySlot.start_time}
                                        onValueChange={(value) => handleTimeChange(displaySlot.id, "start_time", value)}
                                      >
                                        <SelectTrigger className="h-6 text-xs">
                                          <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                          {TIME_SLOTS.map((time) => (
                                            <SelectItem key={time} value={time}>
                                              {time}
                                            </SelectItem>
                                          ))}
                                        </SelectContent>
                                      </Select>
                                      <Select
                                        value={displaySlot.end_time}
                                        onValueChange={(value) => handleTimeChange(displaySlot.id, "end_time", value)}
                                      >
                                        <SelectTrigger className="h-6 text-xs">
                                          <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                          {TIME_SLOTS.map((time) => (
                                            <SelectItem key={time} value={time}>
                                              {time}
                                            </SelectItem>
                                          ))}
                                        </SelectContent>
                                      </Select>
                                    </>
                                  ) : (
                                    <>
                                      <div>{displaySlot.start_time}</div>
                                      <div>{displaySlot.end_time}</div>
                                    </>
                                  )}
                                  {displaySlot.preferred && (
                                    <Badge variant="secondary" className="text-xs">
                                      Preferred
                                    </Badge>
                                  )}
                                </div>
                              ) : (
                                <div className="text-center">Not Available</div>
                              )}
                            </div>
                          ) : (
                            <div className="p-2 bg-gray-200 rounded text-xs text-center text-gray-500">No Data</div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                ),
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Legend */}
      <Card>
        <CardHeader>
          <CardTitle>Legend</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-green-200 border-2 border-green-400 rounded"></div>
              <span className="text-sm">Preferred Time</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-green-100 rounded"></div>
              <span className="text-sm">Available</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-red-100 rounded"></div>
              <span className="text-sm">Not Available</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-gray-200 rounded"></div>
              <span className="text-sm">No Data</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
