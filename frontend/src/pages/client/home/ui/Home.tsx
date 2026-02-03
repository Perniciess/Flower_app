import { Footer } from "@/widgets/footer/ui/Footer";
import { Header } from "@/widgets/header/ui/Header";
import { Hero } from "@/widgets/hero";

export function Home() {
    return (
        <div className="relative flex flex-col">
            <Header />
            <main className="flex-1">
                <Hero />
            </main>
            <Footer />
        </div>
    );
}
