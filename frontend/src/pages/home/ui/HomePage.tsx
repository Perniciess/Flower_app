import { Footer } from "@/widgets/footer/ui/Footer";
import { Header } from "@/widgets/header/ui/Header";

export function HomePage() {
    return (
        <div className="flex min-h-screen flex-col">
            <Header />
            <main className="flex-1">
                <h1>Flower Shop</h1>
            </main>
            <Footer />
        </div>
    );
}
