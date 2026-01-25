'use client'
import { useEffect, useRef } from 'react'

export default function MessageList({ messages = [] }: { messages: any[] }) {
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  return (
    <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((msg: any, i: number) => (
        <div key={i} className="p-2 border rounded">
          {msg.content}
        </div>
      ))}
    </div>
  )
}
