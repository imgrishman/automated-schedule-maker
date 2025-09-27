"use client"

import type React from "react"

import { useState } from "react"
import { useAuth } from "@/hooks/useAuth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Calendar, Users, BarChart3, Zap, AlertCircle } from "lucide-react"

export default function LoginForm() {
  const { login, demoLogin } = useAuth()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    try {
      await login(email, password)
    } catch (error) {
      console.error("Login failed:", error)
      if (error instanceof Error) {
        if (error.message.includes("Cannot connect to server")) {
          setError(
            "Cannot connect to the backend server. Please ensure the Python backend is running on http://localhost:8000\n\nTo start the backend: Run 'python main.py' in the backend directory",
          )
        } else {
          setError(error.message)
        }
      } else {
        setError("Login failed. Please try again.")
      }
    } finally {
      setLoading(false)
    }
  }

  const handleDemoLogin = async (type: "admin" | "employee") => {
    setLoading(true)
    setError("")

    try {
      await demoLogin(type)
    } catch (error) {
      console.error("Demo login failed:", error)
      if (error instanceof Error) {
        if (error.message.includes("Cannot connect to server")) {
          setError(
            "Cannot connect to the backend server. Please ensure the Python backend is running on http://localhost:8000\n\nTo start the backend: Run 'python main.py' in the backend directory",
          )
        } else {
          setError(error.message)
        }
      } else {
        setError("Demo login failed. Please try again.")
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid lg:grid-cols-2 gap-8 items-center">
        {/* Left side - Hero */}
        <div className="text-center lg:text-left">
          <div className="mb-8">
            <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 mb-4">Automated Schedule Planner</h1>
            <p className="text-xl text-gray-600 mb-8">
              AI-powered workforce scheduling that optimizes your team's productivity
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
              <div className="flex items-center gap-3 p-4 bg-white rounded-lg shadow-sm">
                <Calendar className="w-8 h-8 text-blue-600" />
                <div>
                  <h3 className="font-semibold">Smart Scheduling</h3>
                  <p className="text-sm text-gray-600">AI-optimized shifts</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-4 bg-white rounded-lg shadow-sm">
                <Users className="w-8 h-8 text-green-600" />
                <div>
                  <h3 className="font-semibold">Team Management</h3>
                  <p className="text-sm text-gray-600">Centralized control</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-4 bg-white rounded-lg shadow-sm">
                <BarChart3 className="w-8 h-8 text-purple-600" />
                <div>
                  <h3 className="font-semibold">Analytics</h3>
                  <p className="text-sm text-gray-600">Data-driven insights</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right side - Login Form */}
        <div className="w-full max-w-md mx-auto">
          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">Welcome Back</CardTitle>
              <CardDescription>Sign in to your account or try a demo</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription className="whitespace-pre-line">{error}</AlertDescription>
                </Alert>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? "Signing in..." : "Sign In"}
                </Button>
              </form>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-white px-2 text-gray-500">Or try demo</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Button
                  variant="outline"
                  onClick={() => handleDemoLogin("admin")}
                  disabled={loading}
                  className="flex flex-col items-center gap-1 h-auto py-3"
                >
                  <Zap className="w-4 h-4" />
                  <span className="text-xs">Admin Demo</span>
                </Button>
                <Button
                  variant="outline"
                  onClick={() => handleDemoLogin("employee")}
                  disabled={loading}
                  className="flex flex-col items-center gap-1 h-auto py-3"
                >
                  <Users className="w-4 h-4" />
                  <span className="text-xs">Employee Demo</span>
                </Button>
              </div>

              <div className="text-center space-y-2">
                <p className="text-sm text-gray-600">Demo Accounts:</p>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between">
                    <Badge variant="secondary">Admin</Badge>
                    <span className="text-gray-500">admin@asp.com / admin123</span>
                  </div>
                  <div className="flex justify-between">
                    <Badge variant="secondary">Employee</Badge>
                    <span className="text-gray-500">demo@asp.com / demo123</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
