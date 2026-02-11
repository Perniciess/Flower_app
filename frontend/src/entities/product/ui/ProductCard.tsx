"use client";
import type { ProductCardProprs } from "../model/productType";
import Image from "next/image";
import { useProductQuery } from "../api/useProduct";

export function ProductCard({ product_id }: ProductCardProprs) {
    const { data: product, isPending } = useProductQuery(product_id);

    if (isPending)
        return <div className="py-10 text-center">Загрузка…</div>;
    if (!product)
        return null;

    const imagePath = product.images?.[0]?.url;
    const apiUrl = "http://localhost:8000";
    return (
        <div className="flex w-78.75 flex-col items-center gap-4 rounded-lg bg-white p-4 shadow-card">
            <div className="relative h-59.5 w-full overflow-hidden rounded-lg bg-gray-100">

                <Image
                    src={`${apiUrl}${imagePath}`}
                    alt={product.name}
                    fill
                    className="object-cover"
                    unoptimized
                />

            </div>

            <div className="w-full text-center">
                <div className="font-medium">{product.name}</div>
                {/* цена/кнопки сюда */}
            </div>
        </div>
    );
}
