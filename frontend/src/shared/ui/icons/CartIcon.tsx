import type { SVGProps } from "react";

export function CartIcon(props: SVGProps<SVGSVGElement>) {
    return (
        <svg
            width="36"
            height="36"
            viewBox="0 0 36 36"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            {...props}
        >
            <g transform="translate(4.5, 3.38)">
                <path
                    d="M7.5 9.75V7.5C7.5 5.70979 8.21116 3.9929 9.47703 2.72703C10.7429 1.46116 12.4598 0.75 14.25 0.75C16.0402 0.75 17.7571 1.46116 19.023 2.72703C20.2888 3.9929 21 5.70979 21 7.5V9.75M1.875 9.75C1.57663 9.75 1.29048 9.86853 1.07951 10.0795C0.868527 10.2905 0.75 10.5766 0.75 10.875V26.0625C0.75 28.1887 2.56125 30 4.6875 30H23.8125C25.9387 30 27.75 28.2766 27.75 26.1504V10.875C27.75 10.5766 27.6315 10.2905 27.4205 10.0795C27.2095 9.86853 26.9234 9.75 26.625 9.75H1.875Z"
                    stroke="white"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
            </g>
        </svg>
    );
}
