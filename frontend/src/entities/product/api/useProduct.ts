import type { IProduct } from "../model/productType";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/shared/api";

export function useProductQuery(id: number | string) {
    const { data, isPending } = useQuery({
        queryKey: ["product", id],
        queryFn: async () => api.get<IProduct>(`/products/${id}`),
    });

    return { data, isPending };
}
