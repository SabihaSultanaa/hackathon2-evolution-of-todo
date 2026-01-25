/** @jsx @tslib */

interface ToolCallProps {
  tool: string
  arguments: Record<string, any>
  timestamp: Date
}

export default function ToolCall({ tool, arguments, timestamp }: ToolCallProps) {
  const getToolDisplayName = (toolName: string): string => {
    switch (toolName) {
      case 'list_tasks':
        return 'Retrieved tasks'
      case 'create_task':
        return 'Created task'
      case 'toggle_status':
        return 'Updated task status'
      case 'remove_task':
        return 'Deleted task'
      default:
        return toolName
    }
  }

  return (
    <div className="mt-2 text-xs">
      <span className="font-medium text-gray-700">
        → {getToolDisplayName(tool)}
      </span>
      {Object.keys(arguments).length > 0 && (
        <span className="text-gray-500 ml-1">
          with {Object.keys(arguments).join(', ')}
        </span>
      )}
    </div>
  )
}
