import type { IBanner } from "../model/bannerType";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/shared/api";

export function useActiveBannerQuery() {
    const { data, isPending } = useQuery({
        queryKey: ["banner"],
        queryFn: async () => api.get<IBanner[]>("/banners"),
    });

    return { data, isPending };
}
