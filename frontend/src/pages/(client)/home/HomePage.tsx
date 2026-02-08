import { Banners } from "@/widgets/banner";
import { Footer } from "@/widgets/footer";
import { Header } from "@/widgets/header";
import { Hero } from "@/widgets/hero";

export function HomePage() {
    return (
        <div className="relative flex min-h-screen flex-col">
            <Header />
            <main className="flex-1">
                <Hero />
                <Banners />
            </main>
            <Footer />
        </div>
    );
}
