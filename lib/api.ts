const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

interface ApiResponse<T = any> {
  data?: T
  error?: string
  message?: string
}

class ApiService {
  private getAuthHeaders(): HeadersInit {
    const token = typeof window !== "undefined" ? localStorage.getItem("asp_token") : null
    return {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    }
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`
    const config: RequestInit = {
      headers: this.getAuthHeaders(),
      ...options,
    }

    try {
      console.log(`🌐 Making request to: ${url}`)
      const response = await fetch(url, config)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "Request failed" }))
        throw new Error(`API Error: ${response.status} - ${errorData.detail || response.statusText}`)
      }

      const data = await response.json()
      console.log(`✅ Request successful:`, data)
      return data
    } catch (error) {
      console.error(`❌ Request failed:`, error)
      if (error instanceof TypeError && error.message.includes("fetch")) {
        throw new Error("Cannot connect to server. Please ensure the backend is running.")
      }
      throw error
    }
  }

  // Auth endpoints
  async login(credentials: { email: string; password: string }) {
    return this.request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(credentials),
    })
  }

  async demoLogin(type: "admin" | "employee") {
    return this.request(`/api/auth/demo-login?demo_type=${type}`, {
      method: "POST",
    })
  }

  // Employee endpoints
  async getEmployees() {
    return this.request("/api/employees/")
  }

  async getMyProfile() {
    return this.request("/api/employees/me")
  }

  async createEmployee(data: any) {
    return this.request("/api/employees/", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  async updateEmployee(id: string, data: any) {
    return this.request(`/api/employees/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  // Schedule endpoints
  async getSchedules() {
    return this.request("/api/schedules/")
  }

  async getSchedule(id: string) {
    return this.request(`/api/schedules/${id}`)
  }

  async generateSchedule(data: any) {
    return this.request("/api/schedules/generate", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  async publishSchedule(id: string) {
    return this.request(`/api/schedules/${id}/publish`, {
      method: "PUT",
    })
  }

  async getEmployeeSchedule(employeeId: string) {
    return this.request(`/api/schedules/employee/${employeeId}`)
  }

  // Availability endpoints
  async getAvailability() {
    return this.request("/api/availability/")
  }

  async getEmployeeAvailability(employeeId: string) {
    return this.request(`/api/availability/employee/${employeeId}`)
  }

  async createAvailability(data: any) {
    return this.request("/api/availability/", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  async updateAvailability(id: string, data: any) {
    return this.request(`/api/availability/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  }

  // Analytics endpoints
  async getDashboardAnalytics() {
    return this.request("/api/analytics/dashboard")
  }

  async getEmployeeSatisfaction() {
    return this.request("/api/analytics/employee-satisfaction")
  }

  async getScheduleEfficiency(days = 30) {
    return this.request(`/api/analytics/schedule-efficiency?days=${days}`)
  }

  async getDepartmentHours() {
    return this.request("/api/analytics/department-hours")
  }

  async getAIInsights() {
    return this.request("/api/analytics/ai-insights")
  }

  // Health check
  async healthCheck() {
    return this.request("/api/health")
  }
}

export const apiService = new ApiService()
