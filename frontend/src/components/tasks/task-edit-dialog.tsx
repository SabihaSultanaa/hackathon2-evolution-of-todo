"use client"

import { useState } from "react"
import { api, type Task, type TaskUpdate } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Loader2, Pencil } from "lucide-react"
import { toast } from "sonner"

interface TaskEditDialogProps {
  task: Task
  onTaskUpdated?: () => void
}

export function TaskEditDialog({ task, onTaskUpdated }: TaskEditDialogProps) {
  const [open, setOpen] = useState(false)
  const [title, setTitle] = useState(task.title)
  const [description, setDescription] = useState(task.description || "")
  const [isLoading, setIsLoading] = useState(false)

  const handleSave = async () => {
    if (!title.trim()) {
      toast.error("Title is required")
      return
    }

    setIsLoading(true)

    try {
      const updateData: TaskUpdate = {
        title: title.trim(),
        description: description.trim() || undefined,
      }

      await api.updateTask(task.id, updateData)
      toast.success("Task updated")
      setOpen(false)
      onTaskUpdated?.()
    } catch (error) {
      const message = error instanceof Error ? error.message : "Failed to update task"
      toast.error(message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleOpenChange = (isOpen: boolean) => {
    if (!isOpen) {
      setTitle(task.title)
      setDescription(task.description || "")
    }
    setOpen(isOpen)
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm">
          <Pencil className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit Task</DialogTitle>
          <DialogDescription>
            Make changes to your task here. Click save when you're done.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="edit-title">Title</Label>
            <Input
              id="edit-title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What needs to be done?"
              disabled={isLoading}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-description">Description (optional)</Label>
            <Input
              id="edit-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add more details..."
              disabled={isLoading}
            />
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={isLoading || !title.trim()}>
            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Save Changes
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
