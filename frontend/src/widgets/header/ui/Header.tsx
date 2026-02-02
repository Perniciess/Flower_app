import Link from "next/link";

const navItems = [
    { label: "Цветы", href: "/flowers" },
    { label: "Розы", href: "/roses" },
    { label: "Поводы", href: "/occasions" },
    { label: "Подарки", href: "/gifts" },
    { label: "Акции", href: "/sales" },
    { label: "О компании", href: "/about" },
];

export function Header() {
    return (
        <header className="bg-transparent">
            <div className="mx-auto flex max-w-6xl items-center justify-center px-4 py-6">
                <nav>
                    <ul className="flex gap-8">
                        {navItems.map(item => (
                            <li key={item.href}>
                                <Link
                                    href={item.href}
                                    className="text-lg text-gray-700"
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
