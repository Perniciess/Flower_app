import Image from "next/image";
import Link from "next/link";
import { navItems } from "../config";

export function Header() {
    return (
        <header className="flex flex-col items-center border-b border-white bg-transparent pb-6 pt-6">
            <Image src="/images/logo_white.png" alt="logo" width={84} height={65} className="mb-3" />
            <div className="px-4">
                <nav>
                    <ul className="flex gap-8">
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
