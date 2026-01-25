/** @jsx @tslib */
'use client'

import ToolCallResult from './ToolCallResult'
import ToolCall from './ToolCall'

interface AssistantMessageProps {
  content: string
  timestamp: Date
  toolCalls?: ToolCall[]
  toolResults?: ToolCallResult[]
}

export default function AssistantMessage({
  content,
  timestamp,
  toolCalls = [],
  toolResults = [],
}: AssistantMessageProps) {
  return (
    <div className="mr-auto bg-background-secondary border rounded-br-2xl-bl p-3 max-w-[80%] shadow-sm">
      {/* Main content */}
      <p className="text-sm whitespace-pre-wrap">{content}</p>

      {/* Tool calls (if any) */}
      {toolCalls.length > 0 && (
        <div className="mt-3 pt-3 border-t">
          <span className="text-xs font-medium text-gray-600">Actions taken:</span>
          {toolCalls.map((toolCall, idx) => (
            <ToolCall key={`${toolCall.tool}-${idx}`} {...toolCall} />
          ))}
        </div>
      )}

      {/* Tool results (if any) */}
      {toolResults.length > 0 && (
        <div className="mt-3 pt-3 border-t">
          {toolResults.map((result, idx) => (
            <ToolCallResult key={`${result.tool}-${idx}`} {...result} />
          ))}
        </div>
      )}

      {/* Timestamp */}
      <span className="text-xs text-gray-500 block mt-2">
        {timestamp.toLocaleTimeString()}
      </span>
    </div>
  )
}
