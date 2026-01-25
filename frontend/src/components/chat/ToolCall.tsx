'use client'

interface ToolCallProps {
  tool: string;
  arguments: string; // This is okay in the interface definition
  timestamp: string;
}

// Renamed 'arguments' to 'args' in the function below to fix the error
export default function ToolCall({ tool, arguments: args, timestamp }: ToolCallProps) {
  const getToolDisplayName = (toolName: string): string => {
    switch (toolName) {
      case 'list_tasks':
        return 'Checking tasks...';
      case 'add_task':
        return 'Adding new task...';
      case 'update_task':
        return 'Updating task...';
      case 'delete_task':
        return 'Deleting task...';
      default:
        return `Using tool: ${toolName}`;
    }
  };

  return (
    <div className="flex items-center gap-2 p-2 text-xs text-gray-500 italic bg-gray-50 rounded border border-dashed">
      <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
      <span>{getToolDisplayName(tool)}</span>
      {args && (
        <span className="opacity-70 truncate max-w-[150px]">
          ({typeof args === 'string' ? args : JSON.stringify(args)})
        </span>
      )}
    </div>
  );
}
