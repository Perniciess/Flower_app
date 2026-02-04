"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { useSessionQuery } from "@/entities/session";
import { ROUTES } from "@/shared/config/routes";

export function AccountPage() {
    const { data: user, isPending } = useSessionQuery();
    const router = useRouter();

    useEffect(() => {
        if (!isPending && !user) {
            router.replace(ROUTES.LOGIN);
        }
    }, [isPending, user, router]);

    if (isPending) {
        return <div>Загрузка...</div>;
    }

    if (!user) {
        return null;
    }

    return (
        <div>
            <h1>{user.name}</h1>
            <p>{user.phone_number}</p>
        </div>
    );
}
