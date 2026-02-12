import type { IProduct, ProductFilters } from "../model/productType";
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

export function useProductsQuery(
    size = 8,
    page = 1,
    filters?: ProductFilters,
) {
    const queryString = buildQueryString(page, size, filters);

    const { data, isPending } = useQuery({
        queryKey: ["products", size, page, filters],
        queryFn: async () => api.get<Page<IProduct>>(`/products/${queryString}`),
    });

    return { data, isPending };
}

function buildQueryString(
    page: number,
    size: number,
    filters?: ProductFilters,
): string {
    const params = new URLSearchParams({
        page: page.toString(),
        size: size.toString(),
    });

    if (filters) {
        const { type, flower_id, name__ilike, color__in, price__gte, price__lte, is_active, in_stock, search, order_by } = filters;

        if (type !== undefined) {
            params.append("type", type);
        }
        if (flower_id !== undefined) {
            params.append("flower_id", flower_id.toString());
        }
        if (name__ilike !== undefined && name__ilike.length > 0) {
            params.append("name__ilike", name__ilike);
        }
        if (color__in !== undefined && color__in.length > 0) {
            color__in.forEach((color) => {
                params.append("color__in", color);
            });
        }
        if (price__gte !== undefined && price__gte.length > 0) {
            params.append("price__gte", price__gte);
        }
        if (price__lte !== undefined && price__lte.length > 0) {
            params.append("price__lte", price__lte);
        }
        if (is_active !== undefined) {
            params.append("is_active", is_active.toString());
        }
        if (in_stock !== undefined) {
            params.append("in_stock", in_stock.toString());
        }
        if (search !== undefined && search.length > 0) {
            params.append("search", search);
        }
        if (order_by !== undefined && order_by.length > 0) {
            order_by.forEach((order) => {
                params.append("order_by", order);
            });
        }
    }

    return `?${params.toString()}`;
}
