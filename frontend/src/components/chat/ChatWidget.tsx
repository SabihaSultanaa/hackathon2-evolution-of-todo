'use client'

import { useState, useRef, useEffect } from 'react'
import { Bot, User, ArrowRight, BotIcon } from 'lucide-react'
import { API_BASE_URL } from '@/lib/api'

interface ConversationMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export interface RefreshEvent {
  event_type: string
  operation_type: string
  timestamp: Date
}

interface ChatWidgetProps {
  isOpen?: boolean
  onToggle?: () => void
  className?: string
  sessionToken?: string
  onRefreshEvent?: (event: RefreshEvent) => void
}

export default function ChatWidget({
  isOpen = true,
  onToggle,
  className = '',
  sessionToken,
  onRefreshEvent,
}: ChatWidgetProps) {
  const [messages, setMessages] = useState<ConversationMessage[]>([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, isLoading])

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return

    const messageToSend = inputText
    setInputText('')

    const userMessage: ConversationMessage = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: messageToSend,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(sessionToken && { Authorization: `Bearer ${sessionToken}` }),
        },
        body: JSON.stringify({ message: messageToSend }),
      })

      if (!response.ok) {
        throw new Error('Failed to talk to AI')
      }

      const data = await response.json()

      const assistantMessage: ConversationMessage = {
        id: `ai_${Date.now()}`,
        role: 'assistant',
        content:
          data.response ||
          data.message ||
          "I'm not sure how to respond to that.",
        timestamp: new Date(),
      }

      setMessages(prev => [...prev, assistantMessage])

      if (data.requires_refresh) {
        onRefreshEvent?.({
          event_type: 'refresh-event',
          operation_type: 'update',
          timestamp: new Date(),
        })
      }
    } catch (error) {
      console.error('Chat error:', error)
      setMessages(prev => [
        ...prev,
        {
          id: `error_${Date.now()}`,
          role: 'assistant',
          content: "Sorry, I'm having trouble connecting to the server.",
          timestamp: new Date(),
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  if (!isOpen && !onToggle) return null

  return (
    <div
      className={`fixed bottom-4 right-4 w-86 max-h-[600px] flex flex-col rounded-2xl shadow-2xl bg-white border border-blue-900 z-50 ${className}`}
    >
      {/* Header */}
      <div className="p-4 border-b flex justify-between items-center bg-gradient-to-r from-blue-900 to-blue-600 text-white rounded-t-2xl">
        <div className="flex items-center gap-3">
          <BotIcon className="w-8 h-8" />
          <div>
            <h2 className="text-lg font-semibold">AI Assistant</h2>
            <p className="text-xs">Powered by GPT-4</p>
          </div>
        </div>
        {onToggle && (
          <button onClick={onToggle} className="hover:text-black p-1">
            ✕
          </button>
        )}
      </div>

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-100 min-h-[300px]"
      >
        {messages.length === 0 ? (
          <div className="text-center text-gray-700 py-8">
            <p>Hi! I'm your AI task assistant.</p>
            <p className="text-sm">Try: "Add a task to buy milk"</p>
          </div>
        ) : (
          messages.map(msg => (
            <div
              key={msg.id}
              className={`flex items-start gap-3 ${
                msg.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-blue-700 flex items-center justify-center text-white flex-shrink-0">
                  <Bot size={20} />
                </div>
              )}
              <div
                className={`p-3 rounded-lg max-w-[85%] ${
                  msg.role === 'user'
                    ? 'ml-auto bg-gradient-to-r from-blue-900 to-blue-600 text-white border-white'
                    : 'mr-auto  text-black border border-white bg-white'
                }`}
              >
                {msg.content}
              </div>
              {msg.role === 'user' && (
                <div className="w-7 h-7 rounded-full bg-blue-700 flex items-center justify-center flex-shrink-0 text-white">
                  <User size={18} />
                </div>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="text-xs text-black italic text-center">
            AI is thinking...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-gradient-to-r from-blue-900 to-blue-600 rounded-b-2xl">
        <div className="flex gap-2">
          <textarea
            value={inputText}
            onChange={e => setInputText(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Type a message..."
            className="flex-1 p-2 border rounded-lg resize-none focus:ring-1 focus:ring-white outline-none text-sm text-white"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputText.trim()}
            className="bg-white text-blue-700 p-2 rounded-full font-bold hover:bg-blue-200 disabled:bg-blue-100 flex items-center justify-center"
          >
            <ArrowRight size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}
