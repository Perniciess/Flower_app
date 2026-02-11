import type { IProduct } from "../model/productType";
import type { Page } from "@/shared/types/apiTypes";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/shared/api";

export function useProductQuery(productId: number) {
    const { data, isPending } = useQuery({
        queryKey: ["product", productId],
        queryFn: async () => api.get<IProduct>(`/products/${productId}`),
    });

    return { data, isPending };
}

export function useProductsQuery(size = 10, page = 1) {
    const { data, isPending } = useQuery({
        queryKey: ["products", size, page],
        queryFn: async () => api.get<Page<IProduct>>(`/products/?page=${page}&size=${size}`),
    });

    return { data, isPending };
}
