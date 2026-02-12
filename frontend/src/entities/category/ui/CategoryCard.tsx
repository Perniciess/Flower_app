import type { CategoryCardProps } from "../model/categoryType";
import Image from "next/image";

export function CategoryCard({ category }: CategoryCardProps) {
    const imagePath = category.image_url;
    const apiUrl = "http://localhost:8000";

    return (
        <div className="relative flex h-[300px] w-[315px] flex-col items-start justify-end gap-2.5 rounded-2xl overflow-hidden p-[15px_12px]">
            <Image
                src={`${apiUrl}${imagePath}`}
                alt={category.name}
                fill
                className="object-cover -z-10"
                unoptimized
            />
            <div className="absolute inset-0 bg-linear-to-b from-transparent to-black/20 -z-5" />
            <p className="text-white font-medium">{category.name}</p>
        </div>
    );
}
