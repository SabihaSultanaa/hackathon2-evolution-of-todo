'use client'
import { useEffect, useRef } from 'react'

export default function MessageList({ messages = [] }: { messages: any[] }) {
  const scrollRef = useRef<HTMLDivElement>(null)

  // This automatically scrolls the chat to the bottom when a new message arrives
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  return (
    <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4 min-h-[300px]">
      {messages.length === 0 ? (
        <p className="text-center text-gray-500 mt-4">No messages yet. Start a conversation!</p>
      ) : (
        messages.map((msg: any, i: number) => (
          <div 
            key={i} 
            className={`p-3 rounded-lg max-w-[80%] ${
              msg.role === 'user' 
                ? 'bg-blue-600 text-white ml-auto' 
                : 'bg-gray-200 text-gray-800 mr-auto'
            }`}
          >
            <p className="text-sm font-semibold mb-1">
              {msg.role === 'user' ? 'You' : 'AI Agent'}
            </p>
            <p className="text-sm leading-relaxed">
              {msg.content || "..."}
            </p>
          </div>
        ))
      )}
    </div>
  )
}
