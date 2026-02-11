import Image from "next/image";
import Link from "next/link";
import { ROUTES } from "@/shared/config/routes";
import { CartIcon, LikeIcon, SearchIcon, UserIcon } from "@/shared/ui/icons";
import { navItems } from "../config";

export function Header() {
    return (
        <header className="absolute top-0 left-0 z-20 flex h-34.35 w-full flex-col items-center border-b border-white bg-transparent pt-4.25 pb-3.25">
            <div className="flex w-full items-start justify-center px-10">
                <Image
                    src="/images/logo_white.png"
                    alt="logo"
                    width={84}
                    height={65}
                    quality={100}
                    unoptimized
                />
                <div className="absolute right-14.75 top-8.5 flex items-center gap-5">
                    <Link href="">
                        {" "}
                        <SearchIcon />
                    </Link>

                    <Link href={ROUTES.LIKES}>
                        <LikeIcon />
                    </Link>
                    <Link href={ROUTES.ACCOUNT}>
                        <UserIcon />
                    </Link>
                    <Link href={ROUTES.CART}>
                        <CartIcon />
                    </Link>
                </div>
            </div>
            <nav className="mt-[23px]">
                <ul className="flex items-center gap-12.5">
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
