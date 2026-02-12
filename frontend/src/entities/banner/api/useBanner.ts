import type { IBanner } from "../model/bannerType";
import type { Page } from "@/shared/types/apiTypes";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/shared/api";

export function useActiveBannerQuery(
    size = 2,
    page = 1,
) {
    const { data, isPending } = useQuery({
        queryKey: ["banners", size, page],
        queryFn: async () => api.get<Page<IBanner>>(`/banners?size=${size}&page=${page}`),
    });

    return { data, isPending };
}
