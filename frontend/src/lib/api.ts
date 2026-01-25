import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"

// --- INTERFACES ---
export interface Task {
  id: number
  title: string
  description: string
  category: string
  completed: boolean
  user_id: number
  created_at: string
  updated_at: string
}

export interface TaskListResponse {
  tasks: Task[]
}

export interface TaskCreate {
  title: string
  description?: string
  category?: string
}

export interface TaskUpdate {
  title?: string
  description?: string
  category?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface UserRegister {
  email: string
  password: string
}

export interface UserLogin {
  email: string
  password: string
}

// --- API CLIENT ---
class ApiClient {
  private baseUrl: string
  private token: string | null = null

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  // SAVES THE KEY TO THE BROWSER
  setToken(token: string | null) {
    this.token = token
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('auth_token', token)
      } else {
        localStorage.removeItem('auth_token')
      }
    }
  }

  // RETRIEVES THE KEY
  getToken(): string | null {
    if (this.token) return this.token
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token')
    }
    return null
  }

  // CENTRAL REQUEST HANDLER (Handles headers and errors)
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken()
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }), // Forces Bearer format
      ...options.headers,
    }

    const url = `${this.baseUrl}${endpoint}`;
    console.log(`[API] Fetching: ${url}`);
    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || `HTTP error ${response.status}`)
    }

    if (response.status === 204) {
      return {} as T
    }

    return response.json()
  }

  // REGISTER: Now saves the token immediately
  async register(data: UserRegister): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    })
    if (response.access_token) {
      this.setToken(response.access_token)
    }
    return response
  }

  // LOGIN: Fixed to use the internal request system
  async login(data: UserLogin): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    if (response.access_token) {
      this.setToken(response.access_token);
    }
    
    return response;
  }

  logout() {
    this.setToken(null)
  }

  // --- TASK METHODS ---
  async getTasks(): Promise<TaskListResponse> {
    return this.request<TaskListResponse>('/api/v1/tasks')
  }

  async createTask(data: TaskCreate): Promise<Task> {
    return this.request<Task>('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateTask(taskId: number, data: TaskUpdate): Promise<Task> {
    return this.request<Task>(`/api/v1/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async toggleTask(taskId: number): Promise<Task> {
    return this.request<Task>(`/api/v1/tasks/${taskId}/toggle`, {
      method: 'PATCH',
    })
  }

  async deleteTask(taskId: number): Promise<void> {
    return this.request<void>(`/api/v1/tasks/${taskId}`, {
      method: 'DELETE',
    })
  }
}

export const api = new ApiClient()