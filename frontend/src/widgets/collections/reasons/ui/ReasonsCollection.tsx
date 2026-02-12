"use client";

import { useEffect, useRef } from "react";
import { CategoryCard, useActiveCategoryQuery } from "@/entities/category";
import { ArrowLeft, ArrowRight } from "@/shared/ui/icons";

export function ReasonsCollection() {
    const { data: categories, isPending } = useActiveCategoryQuery();
    const scrollContainerRef = useRef<HTMLDivElement>(null);

    const getMaxScroll = () => {
        const container = scrollContainerRef.current;
        if (!container || !categories)
            return 0;

        const rightPadding = 200;

        const maxScroll = Math.max(0, container.scrollWidth - container.clientWidth - rightPadding);

        return maxScroll;
    };

    const scroll = (direction: "left" | "right") => {
        const container = scrollContainerRef.current;
        if (!container || !categories)
            return;

        const scrollAmount = 335;
        const maxScroll = getMaxScroll();

        let newScrollLeft = container.scrollLeft + (direction === "left" ? -scrollAmount : scrollAmount);

        if (newScrollLeft < 0) {
            newScrollLeft = 0;
        }
        else if (newScrollLeft > maxScroll) {
            newScrollLeft = maxScroll;
        }

        container.scrollTo({
            left: newScrollLeft,
            behavior: "smooth",
        });
    };

    useEffect(() => {
        const container = scrollContainerRef.current;
        if (!container || !categories)
            return;

        const handleScroll = () => {
            const rightPadding = 200;

            const maxScroll = Math.max(0, container.scrollWidth - container.clientWidth - rightPadding);

            if (container.scrollLeft > maxScroll) {
                container.scrollTo({
                    left: maxScroll,
                    behavior: "auto",
                });
            }
            if (container.scrollLeft < 0) {
                container.scrollTo({
                    left: 0,
                    behavior: "auto",
                });
            }
        };

        container.addEventListener("scroll", handleScroll);
        return () => container.removeEventListener("scroll", handleScroll);
    }, [categories]);

    if (isPending)
        return <div className="py-10 text-center">Загрузка...</div>;

    return (
        <section className="mt-[80px] flex flex-col items-center">
            <div className="w-full max-w-[1440px]">
                <div className="mb-[33px] relative">
                    <p className="text-center text-[32px] font-medium leading-none">Цветы на любой случай</p>
                    <div className="absolute right-[60px] top-0 flex items-center gap-2">
                        <button
                            onClick={() => scroll("left")}
                            className="flex items-center justify-center text-black hover:text-gray-600 transition-colors"
                            aria-label="Прокрутить влево"
                        >
                            <ArrowLeft stroke="currentColor" />
                        </button>
                        <button
                            onClick={() => scroll("right")}
                            className="flex items-center justify-center text-black hover:text-gray-600 transition-colors"
                            aria-label="Прокрутить вправо"
                        >
                            <ArrowRight stroke="currentColor" />
                        </button>
                    </div>
                </div>
                <div
                    ref={scrollContainerRef}
                    className="flex gap-x-[20px] overflow-x-auto pb-4 pl-[60px] pr-[200px] scrollbar-hide"
                >
                    {categories?.map(category => (
                        <div key={category.id} className="shrink-0">
                            <CategoryCard category={category} />
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
