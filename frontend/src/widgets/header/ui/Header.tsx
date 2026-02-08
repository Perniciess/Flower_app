import Image from "next/image";
import Link from "next/link";
import { ROUTES } from "@/shared/config/routes";
import { navItems } from "../config";

export function Header() {
    return (
        <header className="absolute top-0 left-0 z-20 flex h-[137px] w-full flex-col items-center justify-between border-b border-white bg-transparent pt-[17px] pb-[13px]">
            <div className="flex w-full items-start justify-center px-[40px]">
                <Image
                    src="/images/logo_white.png"
                    alt="logo"
                    width={84}
                    height={65}
                    quality={100}
                    unoptimized
                />
                <div className="absolute right-[59px] top-[34px] flex items-center gap-[20px]">
                    <Link href="">
                        {" "}
                        <svg
                            width="36"
                            height="36"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M21.0002 21L16.6572 16.657M16.6572 16.657C17.4001 15.9141 17.9894 15.0322 18.3914 14.0616C18.7935 13.0909 19.0004 12.0506 19.0004 11C19.0004 9.94942 18.7935 8.90911 18.3914 7.93848C17.9894 6.96785 17.4001 6.08591 16.6572 5.34302C15.9143 4.60014 15.0324 4.01084 14.0618 3.6088C13.0911 3.20675 12.0508 2.99982 11.0002 2.99982C9.9496 2.99982 8.90929 3.20675 7.93866 3.6088C6.96803 4.01084 6.08609 4.60014 5.34321 5.34302C3.84288 6.84335 3 8.87824 3 11C3 13.1218 3.84288 15.1567 5.34321 16.657C6.84354 18.1574 8.87842 19.0002 11.0002 19.0002C13.122 19.0002 15.1569 18.1574 16.6572 16.657Z"
                                stroke="white"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                        </svg>
                    </Link>

                    <Link href={ROUTES.LIKES}>
                        <svg
                            width="36"
                            height="36"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M16.5 3.75C19.1667 3.75 21.25 5.82511 21.25 8.5C21.25 10.1384 20.5174 11.6887 19.0752 13.4531C17.6247 15.2276 15.5359 17.1264 12.9463 19.4746L12.9453 19.4756L12 20.335L11.0547 19.4756L11.0537 19.4746L9.20703 17.792C7.45927 16.1844 6.01253 14.7838 4.9248 13.4531C3.48258 11.6887 2.75 10.1384 2.75 8.5C2.75 5.82511 4.83332 3.75 7.5 3.75C9.0132 3.75 10.4779 4.45833 11.4307 5.56836L12 6.23145L12.5693 5.56836C13.5221 4.45833 14.9868 3.75 16.5 3.75Z"
                                stroke="white"
                                strokeWidth="1.5"
                            />
                        </svg>
                    </Link>
                    <Link href={ROUTES.ACCOUNT}>
                        <svg
                            width="36"
                            height="36"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M12 2C6.477 2 2 6.477 2 12C2 17.523 6.477 22 12 22C17.523 22 22 17.523 22 12C22 6.477 17.523 2 12 2Z"
                                stroke="white"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                            <path
                                d="M4.271 18.346C4.271 18.346 6.5 15.5 12 15.5C17.5 15.5 19.73 18.346 19.73 18.346M12 12C12.7956 12 13.5587 11.6839 14.1213 11.1213C14.6839 10.5587 15 9.79565 15 9C15 8.20435 14.6839 7.44129 14.1213 6.87868C13.5587 6.31607 12.7956 6 12 6C11.2043 6 10.4413 6.31607 9.87868 6.87868C9.31607 7.44129 9 8.20435 9 9C9 9.79565 9.31607 10.5587 9.87868 11.1213C10.4413 11.6839 11.2043 12 12 12Z"
                                stroke="white"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                        </svg>
                    </Link>
                    <Link href={ROUTES.CART}>
                        <svg
                            width="36"
                            height="36"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M7.5 8.25V6.75C7.5 5.55653 7.97411 4.41193 8.81802 3.56802C9.66193 2.72411 10.8065 2.25 12 2.25C13.1935 2.25 14.3381 2.72411 15.182 3.56802C16.0259 4.41193 16.5 5.55653 16.5 6.75V8.25M3.75 8.25C3.55109 8.25 3.36032 8.32902 3.21967 8.46967C3.07902 8.61032 3 8.80109 3 9V19.125C3 20.5425 4.2075 21.75 5.625 21.75H18.375C19.7925 21.75 21 20.6011 21 19.1836V9C21 8.80109 20.921 8.61032 20.7803 8.46967C20.6397 8.32902 20.4489 8.25 20.25 8.25H3.75Z"
                                stroke="white"
                                strokeWidth="1.5"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            />
                        </svg>
                    </Link>
                </div>
            </div>
            <nav>
                <ul className="flex items-center gap-[50px]">
                    {navItems.map(item => (
                        <li key={item.href}>
                            <Link
                                href={item.href}
                                className="text-[18px] font-medium leading-none text-white"
                            >
                                {item.label}
                            </Link>
                        </li>
                    ))}
                </ul>
            </nav>
        </header>
    );
}
