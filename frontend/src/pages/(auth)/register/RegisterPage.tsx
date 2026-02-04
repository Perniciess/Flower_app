import { RegisterForm } from "@/features/auth";

export function RegisterPage() {
    return (
        <div className="flex min-h-screen items-center justify-center">
            <div className="w-full max-w-sm px-4">
                <RegisterForm />
            </div>
        </div>
    );
}
