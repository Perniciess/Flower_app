"use client";

import { BannerCard, useActiveBannerQuery } from "@/entities/banner";

export function Banners() {
    const { data: banners, isPending } = useActiveBannerQuery(2, 1);

    if (isPending)
        return <div className="py-10 text-center">Загрузка…</div>;
    if (!banners || banners.items.length === 0)
        return null;

    return (
        <section className="mt-[80px] w-full overflow-hidden">
            <div className="container mx-auto px-4">
                <ul className="flex flex-nowrap md:justify-center gap-5 overflow-x-auto pb-6 scrollbar-hide">
                    {banners.items.map(banner => (
                        <li
                            key={banner.id}
                            className="relative shrink-0 w-162.5 h-87.5 rounded-lg shadow-lg overflow-hidden group bg-gray-100"
                        >
                            <BannerCard banner={banner} />
                        </li>
                    ))}
                </ul>
            </div>
        </section>
    );
}
