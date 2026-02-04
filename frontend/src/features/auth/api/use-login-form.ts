import type { ILoginForm } from "../model/authTypes";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { apiAuth } from "@/shared/api";
import { setAccessToken } from "@/shared/api/base";
import { ROUTES } from "@/shared/config/routes";

export function useLoginForm() {
    const router = useRouter();
    const { register, handleSubmit, reset } = useForm<ILoginForm>({
        mode: "onChange",
    });

    const loginMutation = useMutation({
        mutationKey: ["login"],
        mutationFn: async (data: ILoginForm) =>
            apiAuth.post<{ access_token: string }>("/auth/login", data),
        onSuccess(data) {
            setAccessToken(data.access_token);
            reset();
            void router.push(ROUTES.HOME);
        },
    });

    const errorMessage = loginMutation.error ? "Ошибка авторизации" : undefined;

    return {
        register,
        errorMessage,
        handleSubmit: handleSubmit(data => loginMutation.mutate(data)),
        isPending: loginMutation.isPending,
    };
}
