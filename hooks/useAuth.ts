"use client"

import { useState, useEffect, createContext, useContext, type ReactNode } from "react"
import { apiService } from "@/lib/api"

interface User {
  id: string
  email: string
  name: string
  role: string
  department?: string
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  demoLogin: (type: "admin" | "employee") => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing token on mount
    const token = localStorage.getItem("asp_token")
    const userData = localStorage.getItem("asp_user")

    if (token && userData) {
      try {
        setUser(JSON.parse(userData))
      } catch (error) {
        console.error("Error parsing user data:", error)
        localStorage.removeItem("asp_token")
        localStorage.removeItem("asp_user")
      }
    }
    setLoading(false)
  }, [])

  const login = async (email: string, password: string) => {
    try {
      const response = await apiService.login({ email, password })

      if (response.access_token && response.user) {
        localStorage.setItem("asp_token", response.access_token)
        localStorage.setItem("asp_user", JSON.stringify(response.user))
        setUser(response.user)
      } else {
        throw new Error("Invalid response format")
      }
    } catch (error) {
      console.error("Login error:", error)
      throw error
    }
  }

  const demoLogin = async (type: "admin" | "employee") => {
    try {
      const response = await apiService.demoLogin(type)

      if (response.access_token && response.user) {
        localStorage.setItem("asp_token", response.access_token)
        localStorage.setItem("asp_user", JSON.stringify(response.user))
        setUser(response.user)
      } else {
        throw new Error("Invalid response format")
      }
    } catch (error) {
      console.error("Demo login error:", error)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem("asp_token")
    localStorage.removeItem("asp_user")
    setUser(null)
  }

  const value = {
    user,
    loading,
    login,
    demoLogin,
    logout,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
