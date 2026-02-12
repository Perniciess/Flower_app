import type { BannerCardProps } from "../model/bannerType";
import Image from "next/image";

export function BannerCard({ banner }: BannerCardProps) {
    const imagePath = banner.image_url;
    const apiUrl = "http://localhost:8000";

    return (
        <div className="container mx-auto px-4">
            <div className="absolute inset-0">
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
        </div>
    );
}
