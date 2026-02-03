import type { VariantProps } from "class-variance-authority";
import { Slot } from "@radix-ui/react-slot";
import { cva } from "class-variance-authority";
import * as React from "react";

import { cn } from "@/shared/lib/utils";

const buttonVariants = cva(
    "inline-flex items-center justify-center gap-[10px] whitespace-nowrap rounded-2xl px-[20px] py-[16px] text-[20px] font-normal transition-all disabled:pointer-events-none disabled:opacity-50 outline-none",
    {
        variants: {
            variant: {
                primary: "border border-white bg-white text-black hover:shadow-[0_0_15.4px_rgba(255,255,255,0.27)]",
                secondary: "border border-white bg-transparent text-white hover:bg-white/[0.01] hover:shadow-[0_0_15.4px_rgba(255,255,255,0.27)]",
                big: "bg-[#326964] text-white",
            },
            size: {
                default: "h-[56px]",
            },
        },
        defaultVariants: {
            variant: "primary",
            size: "default",
        },
    },
);

function Button({
    className,
    variant = "default",
    size = "default",
    asChild = false,
    ...props
}: React.ComponentProps<"button">
    & VariantProps<typeof buttonVariants> & {
        asChild?: boolean;
    }) {
    const Comp = asChild ? Slot : "button";

    return (
        <Comp
            data-slot="button"
            data-variant={variant}
            data-size={size}
            className={cn(buttonVariants({ variant, size, className }))}
            {...props}
        />
    );
}

export { Button, buttonVariants };
