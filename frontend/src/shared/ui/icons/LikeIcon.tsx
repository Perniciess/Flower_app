import type { SVGProps } from "react";

export function LikeIcon(props: SVGProps<SVGSVGElement>) {
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
            <g transform="translate(3, 4.5)">
                <g transform="scale(1.5)">
                    <path
                        d="M14.5 0.75C17.1667 0.75 19.25 2.82511 19.25 5.5C19.25 7.13843 18.5174 8.68866 17.0752 10.4531C15.6247 12.2276 13.5359 14.1264 10.9463 16.4746L10.9453 16.4756L10 17.335L9.05469 16.4756L9.05371 16.4746L7.20703 14.792C5.45927 13.1844 4.01253 11.7838 2.9248 10.4531C1.48258 8.68866 0.75 7.13843 0.75 5.5C0.75 2.82511 2.83332 0.75 5.5 0.75C7.0132 0.75 8.47788 1.45833 9.43066 2.56836L10 3.23145L10.5693 2.56836C11.5221 1.45833 12.9868 0.75 14.5 0.75Z"
                        stroke="white"
                        strokeWidth="1"
                    />
                </g>
            </g>
        </svg>

    );
}
