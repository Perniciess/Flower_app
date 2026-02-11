import * as React from "react";

import { cn } from "@/shared/lib/utils";

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
    return (
        <input
            type={type}
            data-slot="input"
            className={cn(
                "h-9 w-full min-w-0 rounded-md border border-[#326964]",
                "bg-transparent px-3 py-1 text-base shadow-xs",
                "placeholder:text-muted-foreground",
                "selection:bg-primary selection:text-primary-foreground",
                "transition-[color,box-shadow] outline-none",
                "file:text-foreground file:inline-flex file:h-7",
                "file:border-0 file:bg-transparent file:text-sm file:font-medium",
                "disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50",
                "dark:bg-input/30",
                "focus-visible:border-[#3C7C76] focus-visible:ring-[#326964]/50 focus-visible:ring-[3px]",
                "aria-invalid:ring-destructive/20 aria-invalid:border-destructive",
                "dark:aria-invalid:ring-destructive/40",
                className,
            )}
            {...props}
        />
    );
}

export { Input };
