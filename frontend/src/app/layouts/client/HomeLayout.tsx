import type { Metadata } from "next";
import { Providers } from "@/app/providers";
import { montserrat } from "@/shared/config/font";
import "@/app/styles/globals.css";

export const metadata: Metadata = {
    title: "KupiBuket74",
    description: "Магазин цветов",
};

export function HomeLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="ru">
            <body className={montserrat.className}>
                <Providers>{children}</Providers>
            </body>
        </html>
    );
}
