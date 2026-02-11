import type { Metadata } from "next";
import { Providers } from "@/app/providers";
import { montserrat } from "@/shared/config/font";
import "@/app/styles/globals.css";

export const metadata: Metadata = {
    title: "KupiBuket74",
    description: "Магазин цветов",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="ru" suppressHydrationWarning>
            <body className={montserrat.className}>
                <Providers>{children}</Providers>
            </body>
        </html>
    );
}
