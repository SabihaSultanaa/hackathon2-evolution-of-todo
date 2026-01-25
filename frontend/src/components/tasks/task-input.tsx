"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { api, type TaskCreate } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Loader2, Plus, X } from "lucide-react"
import { toast } from "sonner"

interface TaskInputProps {
  onTaskCreated?: () => void
}

export function TaskInput({ onTaskCreated }: TaskInputProps) {
  const router = useRouter()
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [showDescription, setShowDescription] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) {
      toast.error("Please enter a task title")
      return
    }
    setIsLoading(true)
    try {
      const taskData: TaskCreate = {
        title: title.trim(),
        description: description.trim() || undefined,
      }
      await api.createTask(taskData)
      toast.success("Task created successfully!")
      setTitle("")
      setDescription("")
      setShowDescription(false)
      onTaskCreated?.()
      router.refresh()
    } catch (error) {
      const message = error instanceof Error ? error.message : "Failed to create task"
      toast.error(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    // 1. Solid White Card with shadow to pop off the dashboard
    <Card className="mb-6 bg-white border-slate-100 shadow-sm overflow-hidden">
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex gap-2">
            <Input
              placeholder="What needs to be done?"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={isLoading}
              // 2. Added text-slate-900 to ensure visibility
              className="flex-1 h-12 rounded-xl border-slate-200 bg-slate-50 text-slate-900 placeholder:text-slate-400 focus:ring-[rgb(0,23,107)] focus:border-[rgb(0,23,107)]"
            />
            <Button 
              type="submit" 
              disabled={isLoading || !title.trim()}
              className="h-12 px-6 bg-[rgb(0,23,107)] hover:bg-blue-900 text-white rounded-xl font-bold shadow-md transition-all active:scale-95"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Plus className="h-5 w-5" />
              )}
            </Button>
          </div>

          {showDescription ? (
            <div className="space-y-3 animate-in fade-in slide-in-from-top-2 duration-200">
              <Input
                placeholder="Add a description (optional)"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={isLoading}
                // 3. Force dark text here too
                className="h-11 rounded-xl border-slate-200 bg-slate-50 text-slate-900 placeholder:text-slate-400"
              />
              <div className="flex gap-2">
                <Button 
                  type="submit" 
                  size="sm" 
                  disabled={isLoading || !title.trim()}
                  className="bg-[rgb(0,23,107)] text-white hover:bg-blue-900 rounded-lg px-4"
                >
                  Save Task
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setShowDescription(false)
                    setDescription("")
                  }}
                  disabled={isLoading}
                  className="text-slate-500 hover:text-red-500 hover:bg-red-50 transition-colors"
                >
                  <X className="mr-1 h-4 w-4" />
                  Cancel
                </Button>
              </div>
            </div>
          ) : (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => setShowDescription(true)}
              disabled={isLoading}
              // 4. Force specific slate color so it doesn't turn white/invisible
              className="text-slate-400 hover:text-[rgb(0,23,107)] font-bold uppercase tracking-widest text-[10px] px-0"
            >
              <Plus className="mr-2 h-3 w-3" />
              Add description
            </Button>
          )}
        </form>
      </CardContent>
    </Card>
  )
}