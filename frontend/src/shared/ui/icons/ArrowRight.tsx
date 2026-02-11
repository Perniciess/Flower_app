import type { SVGProps } from "react";

export function ArrowRight(props: SVGProps<SVGSVGElement>) {
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
                d="M0.500001 5.17533L12.3593 5.16667M7.84133 9.83333L12.5 5.16667L7.84133 0.5"
                stroke="white"
                strokeLinecap="round"
                strokeLinejoin="round"
            />
        </svg>
    );
}
