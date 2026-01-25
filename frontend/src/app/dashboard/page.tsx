"use client"

import { useEffect, useState } from "react"
import { api, Task } from "@/lib/api"
import { useAuth } from "@/lib/auth-context"
import { useRouter } from "next/navigation"
import ChatWidget, { RefreshEvent } from "@/components/chat/ChatWidget"

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [newTaskTitle, setNewTaskTitle] = useState("")
  const [newTaskDesc, setNewTaskDesc] = useState("")
  const [newTaskCategory, setNewTaskCategory] = useState("General")
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null)
  const [editTitle, setEditTitle] = useState("")
  const [editDesc, setEditDesc] = useState("")
  const [editCategory, setEditCategory] = useState("")
  const [filterCategory, setFilterCategory] = useState("All")
  const [chatOpen, setChatOpen] = useState(false)

  const { isAuthenticated, isLoading, sessionToken, logout } = useAuth()
  const router = useRouter()

  const handleSignOut = async () => {
    await logout();
    router.push('/');
  };

  const categories = ["General", "Work", "Personal", "Urgent", "Shopping"]

  // 1. Fetch tasks from the Python Backend
  const loadTasks = async () => {
    try {
      const response = await api.getTasks()
      setTasks(response.tasks)
    } catch (error) {
      console.error("Could not load tasks:", error)
    }
  }

  // 2. Protect the page
  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        loadTasks()
      } else {
        router.push("/login")
      }
    }
  }, [isAuthenticated, isLoading, router])

  // 3. Logic for the "Add Task" button
  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTaskTitle.trim()) return

    try {
      await api.createTask({
        title: newTaskTitle,
        description: newTaskDesc.trim() || undefined,
        category: newTaskCategory
      })
      setNewTaskTitle("")
      setNewTaskDesc("")
      setNewTaskCategory("General")
      loadTasks()
    } catch (error) {
      alert("Failed to add task. Is your Python backend running?")
    }
  }

  // 4. Toggle Task
  const handleToggleTask = async (taskId: number) => {
    try {
      await api.toggleTask(taskId)
      loadTasks()
    } catch (error) {
      console.error("Toggle failed:", error)
    }
  }

  // 5. Delete Task
  const handleDeleteTask = async (id: number) => {
    try {
      await api.deleteTask(id)
      loadTasks()
    } catch (error) {
      console.error("Delete failed:", error)
    }
  }

  // 6. Edit Start
  const startEdit = (task: Task) => {
    setEditingTaskId(task.id)
    setEditTitle(task.title)
    setEditDesc(task.description || "")
    setEditCategory(task.category || "General")
  }

  // 7. Save Edit
  const handleSaveEdit = async () => {
    if (!editingTaskId || !editTitle.trim()) return
    try {
      await api.updateTask(editingTaskId, {
        title: editTitle,
        description: editDesc.trim() || undefined,
        category: editCategory
      })
      setEditingTaskId(null)
      loadTasks()
    } catch (error) {
      console.error("Update failed:", error)
    }
  }

  const filteredTasks = tasks.filter(task =>
    filterCategory === "All" || task.category === filterCategory
  )

  // Handle refresh events from ChatWidget
  const handleRefreshEvent = (event: RefreshEvent) => {
    console.log('Refresh event received:', event)
    loadTasks()
  }

  if (isLoading) return <div className="min-h-screen bg-white flex items-center justify-center text-slate-900 font-bold uppercase tracking-widest animate-pulse">Loading Workspace...</div>

  return (
    <main className="relative min-h-screen bg-white text-slate-900 flex flex-col lg:flex-row">
      {/* Sign Out Button */}
      <button
        onClick={handleSignOut}
        className="absolute top-4 right-4 lg:top-8 lg:right-8 z-20 px-4 lg:px-6 h-10 lg:h-12 bg-gradient-to-r from-blue-700 to-blue-500 rounded-lg lg:rounded-xl text-white font-bold uppercase tracking-widest text-xs transition-all active:scale-95 shadow-lg shadow-pink-900/20 cursor-pointer"
        title="Sign Out"
      >
        Sign Out
      </button>
      {/* Subtle Background Pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-50 z-0" />

      {/* --- LEFT SIDEBAR: HEADER & INPUT --- */}
      <div className="relative z-10 w-full lg:w-[400px] xl:w-[450px] bg-gradient-to-r from-blue-900 to-blue-700 border-r border-blue-800 flex flex-col p-6 lg:p-8 pt-20 lg:pt-12 shadow-2xl lg:h-screen lg:overflow-y-auto">

        <div className="mb-8 lg:mb-12 text-left">
          <h1 className="text-3xl lg:text-4xl font-black uppercase mb-2 text-white">
            My <span className="text-transparent" style={{ WebkitTextStroke: '1.5px #ffffff' }}>Workspace</span>
          </h1>
          <p className="text-white font-bold uppercase text-[10px] lg:text-[12px] tracking-[0.2em]">
            Manage your daily objectives
          </p>
        </div>

        {/* --- TASK INPUT FORM --- */}
        <div className="bg-gray-300 border border-blue-700/50 p-4 lg:p-6 rounded-2xl lg:rounded-[2rem] shadow-sm mb-6 lg:mb-8">
          <form onSubmit={handleAddTask} className="space-y-4">
            <div className="flex flex-col gap-3">
              <input
                type="text"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                placeholder="What needs to be done?"
                className="w-full h-12 lg:h-14 px-5 lg:px-6 rounded-lg lg:rounded-2xl bg-gradient-to-r from-blue-900 to-blue-700 border border-blue-700 text-white placeholder:text-white focus:outline-none focus:ring-2 focus:ring-gray-300 transition-all font-medium"
              />
              <textarea
                value={newTaskDesc}
                onChange={(e) => setNewTaskDesc(e.target.value)}
                placeholder="Add details (optional)..."
                rows={2}
                className="w-full px-5 lg:px-6 py-3 lg:py-4 rounded-lg lg:rounded-2xl bg-gradient-to-r from-blue-900 to-blue-700 border border-blue-700 text-sm text-white placeholder:text-white focus:outline-none focus:ring-2 focus:ring-gray-300 transition-all resize-none"
              />
              <div className="flex gap-3">
                <select
                  value={newTaskCategory}
                  onChange={(e) => setNewTaskCategory(e.target.value)}
                  className="flex-1 h-11 lg:h-12 px-4 rounded-md lg:rounded-xl bg-gradient-to-r from-blue-900 to-blue-700 border border-blue-700 text-sm text-white font-bold focus:outline-none transition-all cursor-pointer"
                >
                  {categories.map(cat => (
                    <option key={cat} value={cat} className="bg-blue-900 text-white font-bold">{cat}</option>
                  ))}
                </select>
                <button
                  type="submit"
                  className="px-6 lg:px-8 h-11 lg:h-12 cursor-pointer bg-blue-400 text-white hover:bg-blue-500 hover:text-white rounded-md lg:rounded-xl font-black uppercase tracking-widest text-xs transition-all active:scale-95 shadow-lg shadow-gray-500"
                >
                  Add
                </button>
              </div>
            </div>
          </form>
        </div>

        <div className="mt-auto">
           <p className="text-white font-black uppercase text-[11px] lg:text-[13px] tracking-widest mb-3 lg:mb-4">Filters</p>
           <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-2 gap-2">
              {["All", ...categories].map(cat => (
                <button
                  key={cat}
                  onClick={() => setFilterCategory(cat)}
                  className={`px-4 py-3 rounded-lg lg:rounded-xl cursor-pointer text-[10px] lg:text-[11px] font-black uppercase tracking-widest transition-all text-left ${
                    filterCategory === cat
                    ? 'bg-blue-400 text-white shadow-md active:scale-95 '
                    : 'bg-blue-600/50 border border-blue-700/50 text-white hover:bg-blue-800'
                  }`}
                >
                  {cat}
                </button>
              ))}
           </div>
        </div>
      </div>

      {/* --- RIGHT CONTENT: TASK LIST --- */}
      <div className="relative z-10 flex-1 bg-slate-50/50 p-6 lg:p-12 lg:overflow-y-auto">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-6 lg:mb-8">
             <h2 className="text-xs sm:text-sm font-black uppercase tracking-[0.2em] text-blue-900">
                Timeline Tasks ({filteredTasks.length})
             </h2>
             <div className="h-[1px] flex-1 bg-slate-200 ml-4 lg:ml-6 opacity-50" />
          </div>

          <div className="space-y-4 pb-20">
            {filteredTasks.length === 0 ? (
              <div className="p-12 sm:p-24 text-center border-2 border-dashed border-slate-400 rounded-2xl sm:rounded-[3rem] text-blue-900 font-black uppercase tracking-widest">
                Workspace Empty
              </div>
            ) : (
              filteredTasks
                .sort((a,b) => Number(a.completed) - Number(b.completed))
                .map((task) => (
                <div
                  key={task.id}
                  className={`group relative p-4 sm:p-6 rounded-2xl sm:rounded-[1rem] bg-white border border-slate-300 transition-all duration-500 shadow-sm hover:shadow-xl hover:border-slate-200 ${task.completed ? '' : 'hover:-translate-y-1'}`}
                >
                  {editingTaskId === task.id ? (
                    <div className="space-y-4">
                      <input
                        className="w-full bg-slate-50 border border-slate-200 rounded-lg sm:rounded-xl p-3 sm:p-4 text-blue-900 font-bold focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        placeholder="Edit task title"
                      />
                      <textarea
                        className="w-full bg-slate-100 border border-slate-200 rounded-lg sm:rounded-xl p-3 sm:p-4 text-sm text-blue-900 focus:outline-none"
                        rows={3}
                        value={editDesc}
                        onChange={(e) => setEditDesc(e.target.value)}
                        placeholder="Edit task description (optional)"
                      />
                      <div className="flex flex-col sm:flex-row gap-2 sm:gap-4 items-center">
                        <select
                          value={editCategory}
                          onChange={(e) => setEditCategory(e.target.value)}
                          className="w-full sm:w-auto h-10 sm:h-11 px-4 rounded-lg sm:rounded-xl bg-slate-100 border cursor-pointer border-slate-200 text-sm text-black font-bold focus:outline-none"
                        >
                          {categories.map(cat => (
                            <option key={cat} value={cat}>{cat}</option>
                          ))}
                        </select>
                        <div className="flex gap-2 w-full sm:w-auto">
                           <button onClick={handleSaveEdit} className="flex-1 sm:flex-none text-[10px] font-black uppercase tracking-widest bg-blue-600 cursor-pointer text-white px-4 sm:px-6 py-2 sm:py-3 rounded-full hover:bg-blue-700 transition-all">Save</button>
                           <button onClick={() => setEditingTaskId(null)} className="flex-1 sm:flex-none text-[10px] font-black uppercase tracking-widest cursor-pointer bg-slate-100 text-black px-4 sm:px-6 py-2 sm:py-3 rounded-full hover:bg-slate-200 transition-all">Cancel</button>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div className="flex items-start gap-3 sm:gap-4 flex-1">
                         <div className="pt-1">
                           <input
                             type="checkbox"
                             checked={task.completed}
                             onChange={() => handleToggleTask(task.id)}
                             className="h-5 w-5 sm:h-6 sm:w-6 rounded-lg accent-blue-600 cursor-pointer border-slate-400 appearance-none checked:appearance-auto  border"
                           />
                         </div>
                         <div className="space-y-1 flex-1">
                           <div className="flex flex-wrap items-center gap-2">
                             <span className={`text-lg sm:text-xl font-bold ${task.completed ? 'line-through text-gray-600' : 'text-blue-900'}`}>
                               {task.title}
                             </span>
                             <span className={`text-[10px] sm:text-[11px] font-black uppercase px-2 sm:px-3 py-1 rounded-md sm:rounded-lg ${task.completed ? 'bg-green-100 text-green-600 border border-green-600' : 'bg-red-100 text-red-700 border border-red-200'}`}>
                               {task.completed ? 'Done' : 'Pending'}
                             </span>
                             <span className="text-[10px] sm:text-[11px] font-black uppercase px-2 sm:px-3 py-1 rounded-md sm:rounded-lg bg-blue-100 text-blue-700 border border-blue-200">
                               {task.category || 'General'}
                             </span>
                           </div>
                           {task.description && (
                             <p className={`text-sm leading-relaxed  ${task.completed ? 'text-black' : 'text-blue-900'}`}>
                               {task.description}
                             </p>
                           )}
                         </div>
                      </div>

                      <div className="flex items-center gap-2 opacity-100 sm:opacity-0 group-hover:opacity-100 transition-all duration-300 self-end sm:self-center">
                        <button
                          onClick={() => startEdit(task)}
                          className="p-2 sm:p-3 bg-blue-100 hover:bg-blue-200 rounded-lg sm:rounded-xl text-slate-900 hover:text-blue-900 transition-all border border-slate-100"
                          title="Edit Task"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>
                        </button>
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          className="p-2 sm:p-3 bg-red-100 hover:bg-red-200 rounded-lg sm:rounded-xl text-red-500 hover:text-red-600 transition-all border border-red-100"
                          title="Delete Task"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Floating Chat Widget */}
      {chatOpen ? (
        <div className="fixed bottom-4 right-4 z-50 w-[calc(100%-2rem)] max-w-md">
          <ChatWidget
            sessionToken={sessionToken || ''}
            onRefreshEvent={handleRefreshEvent}
            isOpen={chatOpen}
            onToggle={() => setChatOpen(!chatOpen)}
          />
        </div>
      ) : (
        <button
          onClick={() => setChatOpen(true)}
          className="fixed bottom-4 right-4 sm:right-10 z-50 bg-blue-800 cursor-pointer text-white rounded-full p-3 sm:p-4 shadow-lg hover:bg-blue-900 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          title="Open Chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        </button>
      )}
    </main>
  )
}
