"use client";

import Image from "next/image";
import { useActiveBannerQuery } from "@/entities/banner";

export function Banners() {
    const { data: banners, isPending } = useActiveBannerQuery();
    const NEXT_PUBLIC_API_URL = "http://localhost:8000";

    if (isPending)
        return <div className="py-10 text-center">Загрузка…</div>;
    if (!banners || banners.length === 0)
        return null;

    return (
        <section className="py-8 w-full overflow-hidden">
            <div className="container mx-auto px-4">
                <ul className="flex flex-nowrap md:justify-center gap-5 overflow-x-auto pb-6 scrollbar-hide">
                    {banners.map(banner => (
                        <li
                            key={banner.id}
                            className="relative shrink-0 w-162.5 h-87.5 rounded-lg shadow-lg overflow-hidden group bg-gray-100"
                        >
                            <div className="absolute inset-0">
                                {typeof banner.image_url === "string" && banner.image_url.length > 0
                                    ? (
                                            <Image
                                                src={`${NEXT_PUBLIC_API_URL}${banner.image_url}`}
                                                alt={banner.title ?? "Banner"}
                                                fill
                                                className="object-cover"
                                                unoptimized
                                            />
                                        )
                                    : (
                                            <div className="w-full h-full flex items-center justify-center text-gray-400">
                                                Нет изображения
                                            </div>
                                        )}
                            </div>

                            <div className="absolute inset-0 z-20 bg-linear-to-t from-black/80 via-transparent to-transparent text-white">
                                <h3 className="absolute left-6 top-6 font-montserrat text-[28px] font-medium leading-none tracking-normal">
                                    {banner.title ?? ""}
                                </h3>
                                {banner.description !== null && banner.description.trim() !== ""
                                    ? (
                                            <p className="absolute bottom-8 left-6 max-w-[80%] font-montserrat text-[28px] font-medium leading-none tracking-normal opacity-95 line-clamp-2">
                                                {banner.description}
                                            </p>
                                        )
                                    : null}
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </section>
    );
}
