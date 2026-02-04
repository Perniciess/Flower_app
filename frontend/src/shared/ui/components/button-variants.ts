import { cva } from "class-variance-authority";

export const buttonVariants = cva(
    "inline-flex items-center justify-center gap-[10px] whitespace-nowrap rounded-2xl px-[20px] py-[16px] text-[20px] font-normal transition-all disabled:pointer-events-none disabled:opacity-50 outline-none",
    {
        variants: {
            variant: {
                white_primary: "border border-white bg-white text-black hover:shadow-[0_0_15.4px_rgba(255,255,255,0.27)]",
                white_secondary: "border border-white bg-transparent text-white hover:bg-white/[0.01] hover:shadow-[0_0_15.4px_rgba(255,255,255,0.27)]",
                teal_primary: "bg-[#326964] text-white hover:bg-[#3C7C76] active:bg-[#115E59]",
            },
            size: {
                default: "h-[56px]",
            },
        },
        defaultVariants: {
            variant: "white_primary",
            size: "default",
        },
    },
);
