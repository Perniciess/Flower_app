"use client";

import type { PopularCollectionProps } from "../model/collectionType";
import { ProductCard, useProductsQuery } from "@/entities/product";
import { Button } from "@/shared/ui/components/button";
import { ArrowRight } from "@/shared/ui/icons";

export function PopularCollection({ title, search }: PopularCollectionProps) {
    const { data: products, isPending } = useProductsQuery(10, 1, {
        search,
    });

    if (isPending)
        return <div className="py-10 text-center">Загрузка...</div>;

    return (
        <section className="mt-[80px] flex flex-col items-center">
            <p className="mb-[33px] text-[32px] font-medium leading-none">{title}</p>
            <div className="grid grid-cols-4 gap-x-5 gap-y-[31px]">
                {products?.items.map(product => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>

            <Button variant="teal_primary" size="small" className="mt-[30px] text-[18px] font-medium leading-none hover:gap-4">
                Смотреть все
                <ArrowRight />
            </Button>
        </section>
    );
}
