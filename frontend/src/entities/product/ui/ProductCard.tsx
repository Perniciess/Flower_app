import type { ProductCardProps } from "../model/productType";
import Image from "next/image";
import { Button } from "@/shared/ui/components/button";

export function ProductCard({ product }: ProductCardProps) {
    const imagePath = product.images[0]?.url ?? "";
    const apiUrl = "http://localhost:8000";

    return (
        <div className="flex h-100.25 w-78.75 flex-col items-center gap-4.5 overflow-hidden rounded-lg bg-white pb-4 shadow-card transition-shadow duration-300 hover:shadow-[0_0_20px_rgba(0,0,0,0.12)]">

            <div className="relative h-59.5 w-full shrink-0 overflow-hidden rounded-lg bg-gray-100">

                <Image
                    src={`${apiUrl}${imagePath}`}
                    alt={product.name}
                    fill
                    className="object-cover object-[65%_85%] scale-[1.01] transition-transform duration-500 ease-out hover:scale-110"
                    unoptimized
                />

            </div>

            <div className="flex h-17.75 shrink-0 grow-0 self-stretch flex-col items-start gap-1.75 px-4">
                <p className="text-[20px] font-medium leading-none">{product.name}</p>
                <p className="text-[16px] font-normal leading-none text-text-secondary">{product.description}</p>
            </div>

            <div className="flex w-full items-center justify-between px-4">
                <p className="text-[20px] font-medium leading-none">
                    {Number.parseFloat(product.price)}
                    {" "}
                    ₽
                </p>
                <Button variant="teal_secondary" size="small" className="hover:gap-4">
                    В корзину
                </Button>
            </div>
        </div>
    );
}
