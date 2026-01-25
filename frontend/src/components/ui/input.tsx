import * as React from "react"

import { cn } from "@/lib/utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      // Inside input.tsx, look for the className
className={cn(
  "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm ...",
  className
)}
      {...props}
    />
  )
}

export { Input }
