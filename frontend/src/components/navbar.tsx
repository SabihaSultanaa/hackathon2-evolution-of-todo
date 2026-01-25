"use client"

import Link from "next/link"
import { useAuth } from "@/lib/auth-context"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/theme-toggle"
import { CheckSquare } from "lucide-react"

export function Navbar() {
  const { isAuthenticated, logout, user } = useAuth()

  return (
    <header className="border-b sticky top-0 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-50">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <CheckSquare className="h-6 w-6" />
          <span className="font-bold text-xl">Todo App</span>
        </Link>

        <nav className="flex items-center space-x-3">
          {isAuthenticated ? (
            <>
              <ThemeToggle />
              <span className="text-sm text-muted-foreground hidden sm:block">
                {user?.email}
              </span>
              <Link href="/dashboard">
                <Button variant="ghost" size="sm">Dashboard</Button>
              </Link>
              <Button variant="outline" size="sm" onClick={logout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <ThemeToggle />
              <Link href="/login">
                <Button variant="ghost" size="sm">Login</Button>
              </Link>
              <Link href="/register">
                <Button size="sm">Sign Up</Button>
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
