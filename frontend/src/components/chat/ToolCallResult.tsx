/** @jsx @tslib */

interface ToolCallResultProps {
  tool: string
  success: boolean
  data?: any
  error?: string
  timestamp: Date
}

export default function ToolCallResult({ tool, success, data, error, timestamp }: ToolCallResultProps) {
  const getResultDisplayName = (toolName: string): string => {
    switch (toolName) {
      case 'list_tasks':
        return 'Task list retrieved'
      case 'create_task':
        return 'Task created'
      case 'toggle_status':
        return 'Task status updated'
      case 'remove_task':
        return 'Task deleted'
      default:
        return `${toolName} completed`
    }
  }

  if (success) {
    return (
      <div className="mt-1 p-2 rounded bg-green-50 border-l-3 border-green-500">
        <span className="text-sm font-medium text-green-800">
          ✓ {getResultDisplayName(tool)}
        </span>
        {data && data.title && (
          <span className="text-sm text-green-700 ml-1">
            : {data.title}
          </span>
        )}
      </div>
    )
  }

  return (
    <div className="mt-1 p-2 rounded bg-red-50 border-l-3 border-red-500">
      <span className="text-sm font-medium text-red-800">
        ✗ {getResultDisplayName(tool)} failed
      </span>
      {error && (
        <span className="text-sm text-red-600 block mt-1">
          {error}
        </span>
      )}
    </div>
  )
}
