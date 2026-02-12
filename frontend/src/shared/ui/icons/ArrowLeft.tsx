import type { SVGProps } from "react";

export function ArrowLeft({ stroke = "white", ...props }: SVGProps<SVGSVGElement> & { stroke?: string }) {
    return (
        <svg
            width="13"
            height="11"
            viewBox="0 0 13 11"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            {...props}
        >
            <path
                d="M12.5 5.17533L0.6407 5.16667M5.15867 9.83333L0.5 5.16667L5.15867 0.5"
                stroke={stroke}
                strokeLinecap="round"
                strokeLinejoin="round"
            />
        </svg>
    );
}
