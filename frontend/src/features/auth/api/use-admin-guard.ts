"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useSessionQuery } from "@/entities/session";
import { ROUTES } from "@/shared/config/routes";

export function useAdminGuard() {
    const { data: user, isPending } = useSessionQuery();
    const router = useRouter();

    useEffect(() => {
        if (isPending)
            return;

        if (!user) {
            router.replace(`${ROUTES.LOGIN}?next=${ROUTES.ADMIN_INDEX}`);
        }
        else if (user.role !== "admin") {
            router.replace(ROUTES.HOME);
        }
    }, [isPending, user, router]);

    return { user, isAllowed: !isPending && user?.role === "admin" };
}
