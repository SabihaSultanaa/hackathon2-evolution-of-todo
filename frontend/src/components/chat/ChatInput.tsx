/** @jsx @tslib */
'use client'

import { useState } from 'react'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  isLoading?: boolean
  disabled?: boolean
}

export default function ChatInput({
  onSendMessage,
  isLoading = false,
  disabled = false,
}: ChatInputProps) {
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim() && !isLoading && !disabled) {
      onSendMessage(input)
      setInput('')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      if (e.shiftKey) {
        // Allow newline with Shift+Enter
        return
      }
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="p-4 border-t">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Type your message... (Enter to send, Shift+Enter for newline)"
        className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        rows={3}
        disabled={disabled || isLoading}
        aria-label="Message input"
      />
      <button
        onClick={handleSend}
        disabled={!input.trim() || isLoading || disabled}
        className="mt-2 w-full py-2 px-4 bg-primary text-white rounded-lg font-medium hover:bg-primary-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        aria-label="Send message"
      >
        {isLoading ? 'Sending...' : 'Send'}
      </button>
    </div>
  )
}
