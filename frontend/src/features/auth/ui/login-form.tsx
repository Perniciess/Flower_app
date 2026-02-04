"use client";

import { Button } from "@/shared/ui/components/button";
import { Field, FieldLabel } from "@/shared/ui/components/field";
import { Input } from "@/shared/ui/components/input";
import { useLoginForm } from "../api/use-login-form";

export function LoginForm() {
    const { handleSubmit, register, isPending, errorMessage } = useLoginForm();
    return (
        <form
            className="flex flex-col gap-8 text-center"
            onSubmit={e => void handleSubmit(e)}
        >
            <Field>
                <FieldLabel
                    htmlFor="phone_number"
                    className="text-[18px] justify-center"
                >
                    Номер телефона
                </FieldLabel>
                <Input
                    id="phone_number"
                    type="tel"
                    placeholder="+7 999 999 99 99"
                    className="h-11 text-lg"
                    maxLength={16}
                    {...register("phone_number", {
                        required: true,
                        minLength: 12,
                        maxLength: 16,
                        pattern: /^\+?\d[\d\s\-()]{9,}$/,
                        onChange: (e: React.ChangeEvent<HTMLInputElement>) => {
                            e.target.value = e.target.value.replace(/[^\d+\s\-()]/g, "");
                        },
                    })}
                />
            </Field>
            <Field>
                <FieldLabel htmlFor="password" className="text-[18px] justify-center">
                    Пароль
                </FieldLabel>
                <Input
                    id="password"
                    type="password"
                    className="h-11 text-lg"
                    autoComplete="current-password"
                    {...register("password", { required: true })}
                />
            </Field>
            <Button variant="teal_primary" type="submit" disabled={isPending}>
                Войти
            </Button>
            {errorMessage != null && (
                <div className="text-rose-600">{errorMessage}</div>
            )}
        </form>
    );
}
