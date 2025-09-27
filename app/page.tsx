"use client"

import { useState, useEffect } from "react"
import { AuthProvider, useAuth } from "@/hooks/useAuth"
import LoginForm from "@/components/LoginForm"
import Dashboard from "@/components/Dashboard"
import EmployeeManagement from "@/components/EmployeeManagement"
import ScheduleManagement from "@/components/ScheduleManagement"
import AvailabilityManagement from "@/components/AvailabilityManagement"
import Analytics from "@/components/Analytics"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Calendar, Users, BarChart3, Clock, LogOut, Menu, X, Wifi, WifiOff } from "lucide-react"
import { apiService } from "@/lib/api"

function ServerStatus() {
  const [isOnline, setIsOnline] = useState(false)
  const [checking, setChecking] = useState(true)

  useEffect(() => {
    const checkServer = async () => {
      try {
        await apiService.healthCheck()
        setIsOnline(true)
      } catch (error) {
        setIsOnline(false)
      } finally {
        setChecking(false)
      }
    }

    checkServer()
    const interval = setInterval(checkServer, 10000) // Check every 10 seconds

    return () => clearInterval(interval)
  }, [])

  if (checking) {
    return (
      <div className="flex items-center gap-2 text-sm text-gray-500">
        <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
        Checking server...
      </div>
    )
  }

  return (
    <div className="flex items-center gap-2 text-sm">
      {isOnline ? (
        <>
          <Wifi className="w-4 h-4 text-green-500" />
          <span className="text-green-600">Server Online</span>
        </>
      ) : (
        <>
          <WifiOff className="w-4 h-4 text-red-500" />
          <span className="text-red-600">Server Offline</span>
        </>
      )}
    </div>
  )
}

function AppContent() {
  const { user, logout, isAuthenticated, loading } = useAuth()
  const [activeTab, setActiveTab] = useState("dashboard")
  const [sidebarOpen, setSidebarOpen] = useState(false)

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="absolute top-4 right-4">
          <ServerStatus />
        </div>
        <LoginForm />
      </div>
    )
  }

  const navigation = [
    { id: "dashboard", name: "Dashboard", icon: BarChart3 },
    { id: "employees", name: "Employees", icon: Users },
    { id: "schedules", name: "Schedules", icon: Calendar },
    { id: "availability", name: "Availability", icon: Clock },
    { id: "analytics", name: "Analytics", icon: BarChart3 },
  ]

  const renderContent = () => {
    switch (activeTab) {
      case "dashboard":
        return <Dashboard />
      case "employees":
        return <EmployeeManagement />
      case "schedules":
        return <ScheduleManagement />
      case "availability":
        return <AvailabilityManagement />
      case "analytics":
        return <Analytics />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />
      )}

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between h-16 px-6 border-b">
          <h1 className="text-xl font-bold text-gray-900">ASP</h1>
          <Button variant="ghost" size="sm" className="lg:hidden" onClick={() => setSidebarOpen(false)}>
            <X className="w-5 h-5" />
          </Button>
        </div>

        <div className="p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <span className="text-blue-600 font-semibold">{user?.name?.charAt(0) || "U"}</span>
            </div>
            <div>
              <p className="font-medium text-gray-900">{user?.name}</p>
              <Badge variant="secondary" className="text-xs">
                {user?.role}
              </Badge>
            </div>
          </div>

          <nav className="space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id)
                    setSidebarOpen(false)
                  }}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors ${
                    activeTab === item.id
                      ? "bg-blue-50 text-blue-700 border border-blue-200"
                      : "text-gray-600 hover:bg-gray-50"
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  {item.name}
                </button>
              )
            })}
          </nav>
        </div>

        <div className="absolute bottom-0 left-0 right-0 p-6 border-t">
          <div className="mb-4">
            <ServerStatus />
          </div>
          <Button variant="outline" className="w-full bg-transparent" onClick={logout}>
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:ml-64">
        {/* Top bar */}
        <div className="bg-white shadow-sm border-b h-16 flex items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" className="lg:hidden" onClick={() => setSidebarOpen(true)}>
              <Menu className="w-5 h-5" />
            </Button>
            <h2 className="text-xl font-semibold text-gray-900 capitalize">{activeTab}</h2>
          </div>

          <div className="flex items-center gap-4">
            <ServerStatus />
            <div className="text-sm text-gray-500">{new Date().toLocaleDateString()}</div>
          </div>
        </div>

        {/* Page content */}
        <main className="p-6">{renderContent()}</main>
      </div>
    </div>
  )
}

export default function Home() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}
