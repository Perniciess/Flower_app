import { Banners } from "@/widgets/banner";
import { PopularCollection, ReasonsCollection } from "@/widgets/collections";
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
                <PopularCollection title="Новая коллекция букетов" />
                <ReasonsCollection />
                <PopularCollection title="Букеты роз" type="flower" flower_id={1} />
            </main>
            <Footer />
        </div>
    );
}
