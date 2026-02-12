import type { BannerCardProps } from "../model/bannerType";
import Image from "next/image";

export function BannerCard({ banner }: BannerCardProps) {
    const imagePath = banner.image_url;
    const apiUrl = "http://localhost:8000";

    return (
        <div className="container mx-auto px-4">
            <div className="absolute inset-0 transition-transform duration-300 ease-out group-hover:scale-105">
                {typeof banner.image_url === "string" && banner.image_url.length > 0
                    ? (
                            <Image
                                src={`${apiUrl}${imagePath}`}
                                alt={banner.title ?? "Banner"}
                                fill
                                className="object-cover"
                                unoptimized
                            />
                        )
                    : (
                            <div className="flex h-full w-full items-center justify-center text-gray-400">
                                Нет изображения
                            </div>
                        )}
            </div>

            <div
                className="absolute inset-0 z-20 text-white"
                style={{
                    background:
                        "linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0.29%, rgba(0, 0, 0, 0) 51.92%, rgba(0, 0, 0, 0.5) 100%)",
                }}
            >
                <h3 className="absolute left-8 top-8 font-montserrat text-[28px] font-medium leading-none tracking-normal transition-transform duration-300 ease-out group-hover:translate-y-2">
                    {banner.title ?? ""}
                </h3>
                {banner.description !== null && banner.description.trim() !== ""
                    ? (
                            <p className="absolute bottom-8 left-8 max-w-[80%] font-montserrat text-[28px] font-medium leading-none tracking-normal opacity-95 line-clamp-2 transition-transform duration-300 ease-out group-hover:-translate-y-2">
                                {banner.description}
                            </p>
                        )
                    : null}
            </div>
            <div
                className="pointer-events-none absolute top-[15px] right-4 bottom-4 left-[15px] z-30 rounded-lg border border-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
                aria-hidden
            />
        </div>
    );
}
