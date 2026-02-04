import type { IRegisterForm } from "../model/authTypes";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { apiAuth } from "@/shared/api";
import { ROUTES } from "@/shared/config/routes";

export function useRegisterForm() {
    const router = useRouter();
    const { register, handleSubmit, reset } = useForm<IRegisterForm>({
        mode: "onChange",
    });

    const loginMutation = useMutation({
        mutationKey: ["register"],
        mutationFn: async (data: IRegisterForm) => apiAuth.post("/auth/register", data),
        onSuccess() {
            reset();
            void router.push(ROUTES.HOME);
        },
    });

    const errorMessage = loginMutation.error ? "Ошибка регистрации" : undefined;

    return {
        register,
        errorMessage,
        handleSubmit: handleSubmit(data => loginMutation.mutate(data)),
        isPending: loginMutation.isPending,
    };
}
