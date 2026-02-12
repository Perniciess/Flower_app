import type { CategoryCardProps } from "../model/categoryType";
import Image from "next/image";

export function CategoryCard({ category }: CategoryCardProps) {
    const imagePath = category.image_url;
    const apiUrl = "http://localhost:8000";

    return (
        <div className="group relative flex h-75 w-78.75 flex-col items-start justify-end overflow-hidden rounded-2xl p-4">
            <div className="absolute inset-0 -z-10 transition-transform duration-300 ease-out group-hover:scale-105">
                <Image
                    src={`${apiUrl}${imagePath}`}
                    alt={category.name}
                    fill
                    className="object-cover"
                    unoptimized
                />
            </div>
            <div className="absolute inset-0 bg-linear-to-b from-transparent to-black/20 -z-5" />
            <p className="relative z-20 text-[28px] font-medium leading-[100%] tracking-normal text-white transition-transform duration-300 ease-out group-hover:translate-x-1 group-hover:-translate-y-2">
                {category.name}
            </p>
            <div
                className="pointer-events-none absolute top-[11px] right-[11px] bottom-[11px] left-[11px] z-10 rounded-lg border border-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
                aria-hidden
            />
        </div>
    );
}
