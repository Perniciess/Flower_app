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

        // Рассчитываем максимальную прокрутку так, чтобы последняя карточка была полностью видна
        // и не появлялось пустое место справа
        //
        // scrollWidth включает весь контент включая padding (left 60px + cards + right 200px)
        // clientWidth - видимая ширина контейнера
        //
        // Когда мы прокручиваем до конца, мы хотим, чтобы:
        // - Последняя карточка была полностью видна
        // - Не было пустого места справа
        //
        // Стандартная формула: maxScroll = scrollWidth - clientWidth
        // Но нужно убедиться, что это значение не позволяет прокрутить дальше, чем нужно
        const standardMaxScroll = container.scrollWidth - container.clientWidth;

        // Проверяем, что стандартный расчет корректен
        // Если scrollWidth включает padding справа (200px), то стандартный расчет должен быть правильным
        // Но для безопасности ограничиваем максимум этим значением
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
        const scrollAmount = 335; // Размер прокрутки за один клик
        const threshold = 2; // Порог для учета погрешностей округления

        // Можно прокрутить влево, если мы не в начале
        const canLeft = scrollLeft > threshold;

        // Можно прокрутить вправо только если:
        // 1. Мы еще не достигли maxScroll (с учетом порога)
        // 2. После прокрутки мы не превысим maxScroll
        // Это предотвращает появление пустого места
        const isNearEnd = scrollLeft >= maxScroll - threshold;
        const wouldExceedMax = scrollLeft + scrollAmount > maxScroll + threshold;
        const canRight = !isNearEnd && !wouldExceedMax;

        return { canScrollLeft: canLeft, canScrollRight: canRight };
    }, [categories, getMaxScroll]);

    const scroll = (direction: "left" | "right") => {
        const container = scrollContainerRef.current;
        if (!container || !categories)
            return;

        // Блокируем прокрутку, если она невозможна
        if (direction === "left" && !canScrollLeft)
            return;
        if (direction === "right" && !canScrollRight)
            return;

        const scrollAmount = 335;
        const maxScroll = getMaxScroll();

        let newScrollLeft = container.scrollLeft + (direction === "left" ? -scrollAmount : scrollAmount);

        // Строго ограничиваем прокрутку границами
        if (newScrollLeft < 0) {
            newScrollLeft = 0;
        }
        else if (newScrollLeft > maxScroll) {
            // Если превышаем максимум, устанавливаем точно на максимум
            newScrollLeft = maxScroll;
        }

        container.scrollTo({
            left: newScrollLeft,
            behavior: "smooth",
        });

        // Обновляем состояние кнопок сразу после установки новой позиции
        // и после завершения анимации прокрутки
        const state = updateScrollButtons();
        setCanScrollLeft(state.canScrollLeft);
        setCanScrollRight(state.canScrollRight);

        setTimeout(() => {
            const updatedState = updateScrollButtons();
            setCanScrollLeft(updatedState.canScrollLeft);
            setCanScrollRight(updatedState.canScrollRight);
        }, 350);
    };

    // Обновление состояния кнопок при изменении прокрутки
    useEffect(() => {
        const container = scrollContainerRef.current;
        if (!container || !categories)
            return;

        const updateState = () => {
            const state = updateScrollButtons();
            setCanScrollLeft(state.canScrollLeft);
            setCanScrollRight(state.canScrollRight);
        };

        // Обновляем состояние кнопок при монтировании
        updateState();

        const handleScroll = () => {
            const maxScroll = getMaxScroll();
            const scrollLeft = container.scrollLeft;

            // Строго ограничиваем прокрутку границами
            if (scrollLeft > maxScroll) {
                container.scrollTo({
                    left: maxScroll,
                    behavior: "auto",
                });
                updateState();
                return;
            }

            // Ensure we don't scroll before the start
            if (scrollLeft < 0) {
                container.scrollTo({
                    left: 0,
                    behavior: "auto",
                });
                updateState();
                return;
            }

            // Когда близко к концу, принудительно устанавливаем на maxScroll
            // Это предотвращает появление пустого места
            const threshold = 2;
            if (maxScroll > 0 && scrollLeft >= maxScroll - threshold && scrollLeft < maxScroll) {
                container.scrollTo({
                    left: maxScroll,
                    behavior: "auto",
                });
            }

            // Обновляем состояние кнопок после прокрутки
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
