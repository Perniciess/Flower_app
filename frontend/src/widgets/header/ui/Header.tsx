import Image from "next/image";
import Link from "next/link";
import { navItems } from "../config";

export function Header() {
    return (
        <header className="absolute top-0 left-0 z-20 flex h-[137px] w-full flex-col items-center justify-between border-b border-white bg-transparent pt-[17px] pb-[13px]">
            <Image src="/images/logo_white.png" alt="logo" width={84} height={65} quality={100} unoptimized className="" />
            <div>
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
            </div>
        </header>
    );
}
