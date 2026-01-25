"use client"

import { useState, useEffect } from "react"
import { api, type Task } from "@/lib/api"
import { Card, CardContent } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { Trash2 } from "lucide-react"
import { toast } from "sonner"
import { TaskEditDialog } from "./task-edit-dialog"

interface TaskListProps {
  onTaskUpdate?: () => void
}

export function TaskList({ onTaskUpdate }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [togglingTask, setTogglingTask] = useState<number | null>(null)

  const fetchTasks = async () => {
    try {
      const response = await api.getTasks()
      setTasks(response.tasks)
    } catch (error) {
      console.error("Failed to fetch tasks:", error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  const handleToggle = async (taskId: number) => {
    // OPTIMISTIC UPDATE: Change UI instantly
    setTasks(prev => prev.map(t => t.id === taskId ? { ...t, completed: !t.completed } : t))
    
    try {
      await api.toggleTask(taskId)
      onTaskUpdate?.()
    } catch (error) {
      fetchTasks() // Revert if failed
      toast.error("Failed to update status")
    }
  }

  const handleDelete = async (taskId: number) => {
    try {
      await api.deleteTask(taskId)
      toast.success("Task deleted")
      fetchTasks()
      onTaskUpdate?.()
    } catch (error) {
      toast.error("Delete failed")
    }
  }

  if (isLoading) return <TaskListSkeleton />

  return (
    <div className="space-y-3">
      {tasks
  .sort((a, b) => Number(a.completed) - Number(b.completed))
  .map((task) => (
    <Card
      key={task.id}
      className={`transition-all duration-300 border-l-4 opacity-100 ${ /* opacity-100 keeps it sharp */
        task.completed 
          ? "bg-green-50/30 border-l-green-600 shadow-none" 
          : "bg-white border-l-yellow-500 shadow-sm border-y border-r"
      }`}
    >
      <CardContent className="py-4 px-5">
        <div className="flex items-center gap-4">
          <Checkbox
            checked={task.completed}
            onCheckedChange={() => handleToggle(task.id)}
            id={`task-${task.id}`}
            className="h-5 w-5 border-2 data-[state=checked]:bg-green-600"
          />
          
          <div className="flex-1">
            <label htmlFor={`task-${task.id}`} className="cursor-pointer">
              <div className="flex items-center gap-3 mb-0.5">
                {/* Text is now slate-900 (dark) even when completed */}
                <span className={`font-semibold ${task.completed ? "text-slate-700" : "text-slate-900"}`}>
                  {task.title}
                </span>
                
                <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${
                  task.completed 
                    ? "bg-green-600 text-white" /* White text on solid green for clarity */
                    : "bg-yellow-100 text-yellow-700 border border-yellow-200"
                }`}>
                  {task.completed ? "✓ Completed" : "Pending"}
                </span>
              </div>

              {task.description && (
                <p className="text-sm text-slate-600">
                  {task.description}
                </p>
              )}
            </label>
          </div>

          <div className="flex items-center gap-1">
            <TaskEditDialog task={task} onTaskUpdated={fetchTasks} />
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleDelete(task.id)}
              className="text-slate-400 hover:text-red-600 hover:bg-red-50"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  ))}
    </div>
  )
}
function TaskListSkeleton() {
  return (
    <div className="space-y-3">
      {Array.from({ length: 3 }).map((_, i) => (
        <Card key={i} className="border-l-4 border-l-slate-200">
          <CardContent className="py-4 px-5">
            <div className="flex items-center gap-4">
              <Skeleton className="h-5 w-5 rounded" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-5 w-1/3" />
                <Skeleton className="h-4 w-1/2" />
              </div>
              <div className="flex gap-2">
                <Skeleton className="h-8 w-8 rounded" />
                <Skeleton className="h-8 w-8 rounded" />
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

// ... Keep your TaskListSkeleton code here ...