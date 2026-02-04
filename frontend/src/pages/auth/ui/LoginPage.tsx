import { LoginForm } from "@/features/auth/ui/login-form";

export function LoginPage() {
    return (
        <div className="flex min-h-screen items-center justify-center">
            <div className="w-full max-w-sm px-4">
                <LoginForm />
            </div>
        </div>
    );
}
