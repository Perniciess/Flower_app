import type { ICategory } from "../model/categoryType";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/shared/api";

export function useActiveCategoryQuery() {
    const { data, isPending } = useQuery({
        queryKey: ["category"],
        queryFn: async () => api.get<ICategory[]>("/category/all_active"),
    });

    return { data, isPending };
}
