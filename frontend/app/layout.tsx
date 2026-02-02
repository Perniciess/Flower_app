import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import { Providers } from "@/app/providers";
import "@/app/styles/globals.css";

const montserrat = Montserrat({
  weight: ['300', '400', '500', '700'],
  subsets: ['latin', 'cyrillic'],
  display:'swap',
  fallback: ['Arial', 'sans-serif'],
});

export const metadata: Metadata = {
    title: "Flower Shop",
    description: "Магазин цветов",
};

export default function RootLayout({
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
