/** @jsx @tslib */
'use client'

interface UserMessageProps {
  content: string
  timestamp: Date
}

export default function UserMessage({ content, timestamp }: UserMessageProps) {
  return (
    <div className="ml-auto bg-primary text-white p-3 rounded-br-2xl-bl max-w-[80%] shadow-sm">
      <p className="text-sm whitespace-pre-wrap">{content}</p>
      <span className="text-xs opacity-70 block mt-1">
        {timestamp.toLocaleTimeString()}
      </span>
    </div>
  )
}
