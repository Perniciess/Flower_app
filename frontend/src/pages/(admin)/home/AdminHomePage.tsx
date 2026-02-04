"use client";
import { useAdminGuard } from "@/features/auth";

export function AdminHomePage() {
    const { user, isAllowed } = useAdminGuard();

    if (!isAllowed) {
        return <div>Загрузка...</div>;
    }

    if (!user) {
        return null;
    }

    return (
        <div>
            ПАНЕЛЬ АДМИНИСТРАТОРА
            <p>{user.phone_number}</p>
        </div>
    );
}
