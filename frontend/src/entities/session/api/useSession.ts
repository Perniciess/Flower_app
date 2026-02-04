import type { IUser } from "@/shared/types/userTypes";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { apiAuth } from "@/shared/api";

export function useSessionQuery() {
    const { data, isPending } = useQuery({
        queryKey: ["user"],
        queryFn: async () => apiAuth.get<IUser>("/users/me"),
    });

    return { data, isPending };
}

export function useResetSession() {
    const queryClient = useQueryClient();
    return () => queryClient.removeQueries({ queryKey: ["user"] });
}
