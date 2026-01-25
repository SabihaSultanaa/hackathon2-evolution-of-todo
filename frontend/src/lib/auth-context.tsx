"use client"

import React, { createContext, useContext, useState, useEffect, useCallback } from "react"
import { api, type UserRegister, type UserLogin } from "@/lib/api"

interface AuthContextType {
  user: { id: number; email: string } | null
  isLoading: boolean
  isAuthenticated: boolean
  register: (data: UserRegister) => Promise<void>
  login: (data: UserLogin) => Promise<void>
  logout: () => void
  error: string | null
  clearError: () => void
  sessionToken: string | null
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<{ id: number; email: string } | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [sessionToken, setSessionToken] = useState<string | null>(null)

  const clearError = useCallback(() => setError(null), [])

  const logout = useCallback(() => {
    api.logout()
    setUser(null)
    setSessionToken(null)
  }, [])

  // FIXED REGISTER: Automatically logs in after creating account
  const register = useCallback(async (data: UserRegister) => {
    setIsLoading(true)
    setError(null)
    try {
      // 1. Create the account in the database
      await api.register(data)
      
      // 2. Automatically log in to get the token immediately
      const authResponse = await api.login({ email: data.email, password: data.password })
      
      // 3. Set the user state so the Dashboard knows you are logged in
      setUser({ id: 1, email: data.email })
      setSessionToken(authResponse.access_token)
    } catch (err: any) {
      const message = err.message || "Registration failed"
      setError(message)
      throw new Error(message)
    } finally {
      setIsLoading(false)
    }
  }, [])

  // FIXED LOGIN: Sets the user state correctly
  const login = useCallback(async (data: UserLogin) => {
    setIsLoading(true)
    setError(null)
    try {
      const authResponse = await api.login(data)
      setUser({ id: 1, email: data.email })
      setSessionToken(authResponse.access_token)
    } catch (err: any) {
      const message = err.message || "Login failed"
      setError(message)
      throw new Error(message) 
    } finally {
      setIsLoading(false)
    }
  }, [])

  // CHECK SESSION: Look for existing token when page refreshes
  useEffect(() => {
    const token = api.getToken()
    if (token) {
      // If a token exists in local storage, assume user is logged in
      setUser({ id: 0, email: "User" })
      setSessionToken(token)
    }
    setIsLoading(false)
  }, [])

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user, // This is what the Dashboard checks
    register,
    login,
    logout,
    error,
    clearError,
    sessionToken,
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