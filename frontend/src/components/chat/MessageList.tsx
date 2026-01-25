/** @jsx @tslib */
'use client'

import { useEffect, useRef } from 'react'
import ConversationMessage, { ConversationMessageProps } from './ConversationMessage'

interface MessageListProps {
  messages: ConversationMessage[]
  isLoading?: boolean
}

export default function MessageList({ messages, isLoading = false }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to latest message
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, isLoading])

  return (
    <div
      ref={scrollRef}
      className="flex-1 overflow-y-auto p-4 space-y-3"
      role="log"
      aria-live="polite"
      aria-label="Chat messages"
    >
      {messages.length === 0 && !isLoading ? (
        <div className="text-center text-gray-500 py-8">
          <p className="text-lg font-medium">Get started with AI-powered task management</p>
          <p className="text-sm mt-2">
            Try asking things like:
          </p>
          <ul className="text-sm mt-3 space-y-1 list-disc list-inside">
            <li>"I need to finish my quarterly report"</li>
            <li>"Show me all my work tasks"</li>
            <li>"I'm done with reviewing code"</li>
          </ul>
        </div>
      ) : (
        messages.map((message) => (
          <ConversationMessage key={message.id} {...message} />
        ))
      )}

      {isLoading && (
        <div className="mr-auto bg-background-secondary rounded-br-2xl-bl p-4 max-w-[80%]">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
            <span className="text-sm text-gray-500">Processing your request...</span>
          </div>
        </div>
      )}
    </div>
  )
}
