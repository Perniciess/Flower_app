import { Footer } from "@/widgets/footer/ui/Footer";
import { Hero } from "@/widgets/hero";

export function HomePage() {
    return (
        <div className="flex min-h-screen flex-col">
            <main className="flex-1">
                <Hero />
            </main>
            <Footer />
        </div>
    );
}
