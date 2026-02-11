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
        <div className="flex h-[401px] w-78.75 flex-col items-center gap-[18px] overflow-hidden rounded-lg bg-white pb-4 shadow-card">
            <div className="relative h-59.5 w-full shrink-0 overflow-hidden rounded-lg">

                <Image
                    src={`${apiUrl}${imagePath}`}
                    alt={product.name}
                    fill
                    className="object-cover object-[65%_85%]"
                    unoptimized
                />

            </div>

            <div className="flex h-[71px] shrink-0 grow-0 self-stretch flex-col items-start gap-[7px] px-4">
                <p className="text-[20px] font-medium leading-none">{product.name}</p>
                <p className="text-[16px] font-normal leading-none text-text-secondary">{product.description}</p>
            </div>

        </div>
    );
}
