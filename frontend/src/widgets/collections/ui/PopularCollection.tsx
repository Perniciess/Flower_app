"use client";

import type { PopularCollectionProps } from "../model/collectionType";
import { ProductCard, useProductsQuery } from "@/entities/product";
import { Button } from "@/shared/ui/components/button";
import { ArrowRight } from "@/shared/ui/icons";

export function PopularCollection({ title, type, flower_id }: PopularCollectionProps) {
    const { data: products, isPending } = useProductsQuery(8, 1, {
        type,
        flower_id,
    });

    if (isPending)
        return <div className="py-10 text-center">Загрузка...</div>;

    return (
        <section className="mt-20 flex flex-col items-center">
            <p className="mb-8.25 text-[32px] font-medium leading-none">{title}</p>
            <div className="grid grid-cols-4 gap-x-5 gap-y-7.75">
                {products?.items.map(product => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>

            <Button variant="teal_primary" size="small" className="mt-7.5 text-[18px] font-medium leading-none hover:gap-4">
                Смотреть все
                <ArrowRight />
            </Button>
        </section>
    );
}
