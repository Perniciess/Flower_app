"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { CategoryCard, useActiveCategoryQuery } from "@/entities/category";
import { ArrowLeft, ArrowRight } from "@/shared/ui/icons";

export function ReasonsCollection() {
    const { data: categories, isPending } = useActiveCategoryQuery();
    const scrollContainerRef = useRef<HTMLDivElement>(null);
    const [canScrollLeft, setCanScrollLeft] = useState(false);
    const [canScrollRight, setCanScrollRight] = useState(true);

    const getMaxScroll = useCallback(() => {
        const container = scrollContainerRef.current;
        if (!container || !categories || categories.length === 0)
            return 0;

        const standardMaxScroll = container.scrollWidth - container.clientWidth;

        const maxScroll = Math.max(0, standardMaxScroll);

        return maxScroll;
    }, [categories]);

    const updateScrollButtons = useCallback(() => {
        const container = scrollContainerRef.current;
        if (!container || !categories || categories.length === 0) {
            return { canScrollLeft: false, canScrollRight: false };
        }

        const maxScroll = getMaxScroll();
        const scrollLeft = container.scrollLeft;
        const scrollAmount = 335;
        const threshold = 2;
        const canLeft = scrollLeft > threshold;
        const isNearEnd = scrollLeft >= maxScroll - threshold;
        const wouldExceedMax = scrollLeft + scrollAmount > maxScroll + threshold;
        const canRight = !isNearEnd && !wouldExceedMax;

        return { canScrollLeft: canLeft, canScrollRight: canRight };
    }, [categories, getMaxScroll]);

    const scroll = (direction: "left" | "right") => {
        const container = scrollContainerRef.current;
        if (!container || !categories)
            return;

        if (direction === "left" && !canScrollLeft)
            return;
        if (direction === "right" && !canScrollRight)
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

        const state = updateScrollButtons();
        setCanScrollLeft(state.canScrollLeft);
        setCanScrollRight(state.canScrollRight);

        setTimeout(() => {
            const updatedState = updateScrollButtons();
            setCanScrollLeft(updatedState.canScrollLeft);
            setCanScrollRight(updatedState.canScrollRight);
        }, 350);
    };

    useEffect(() => {
        const container = scrollContainerRef.current;
        if (!container || !categories)
            return;

        const updateState = () => {
            const state = updateScrollButtons();
            setCanScrollLeft(state.canScrollLeft);
            setCanScrollRight(state.canScrollRight);
        };

        updateState();

        const handleScroll = () => {
            const maxScroll = getMaxScroll();
            const scrollLeft = container.scrollLeft;

            if (scrollLeft > maxScroll) {
                container.scrollTo({
                    left: maxScroll,
                    behavior: "auto",
                });
                updateState();
                return;
            }

            if (scrollLeft < 0) {
                container.scrollTo({
                    left: 0,
                    behavior: "auto",
                });
                updateState();
                return;
            }

            const threshold = 2;
            if (maxScroll > 0 && scrollLeft >= maxScroll - threshold && scrollLeft < maxScroll) {
                container.scrollTo({
                    left: maxScroll,
                    behavior: "auto",
                });
            }

            updateState();
        };

        const handleScrollEnd = () => {
            updateState();
        };

        container.addEventListener("scroll", handleScroll);
        container.addEventListener("scrollend", handleScrollEnd);

        return () => {
            container.removeEventListener("scroll", handleScroll);
            container.removeEventListener("scrollend", handleScrollEnd);
        };
    }, [categories, getMaxScroll, updateScrollButtons]);

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
                            disabled={!canScrollLeft}
                            className={`flex items-center justify-center transition-colors ${
                                canScrollLeft
                                    ? "text-black hover:text-gray-600 cursor-pointer"
                                    : "text-gray-300 cursor-not-allowed"
                            }`}
                            aria-label="Прокрутить влево"
                        >
                            <ArrowLeft stroke="currentColor" />
                        </button>
                        <button
                            onClick={() => scroll("right")}
                            disabled={!canScrollRight}
                            className={`flex items-center justify-center transition-colors ${
                                canScrollRight
                                    ? "text-black hover:text-gray-600 cursor-pointer"
                                    : "text-gray-300 cursor-not-allowed"
                            }`}
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
