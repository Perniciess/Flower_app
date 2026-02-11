import type { ApiRequestInit } from "@/shared/types/apiTypes";
import { useAuthStore } from "@/shared/stores/auth.store";
import { ApiError } from "@/shared/types/apiTypes";
import { buildBody, request } from "./base";
import { withCsrf } from "./interceptors";

export const api = {
    get: async <T>(endpoint: string, options?: ApiRequestInit) =>
        request<T>(endpoint, { ...options, method: "GET" }),

    post: async <T>(endpoint: string, body?: unknown, options?: ApiRequestInit) =>
        request<T>(endpoint, { ...options, method: "POST", body: buildBody(body) }),

    patch: async <T>(
        endpoint: string,
        body?: unknown,
        options?: ApiRequestInit,
    ) =>
        request<T>(endpoint, {
            ...options,
            method: "PATCH",
            body: buildBody(body),
        }),

    delete: async <T>(endpoint: string, options?: ApiRequestInit) =>
        request<T>(endpoint, { ...options, method: "DELETE" }),
};

async function authRequest<T>(
    endpoint: string,
    options: ApiRequestInit = {},
): Promise<T> {
    const opts = withCsrf(options);

    try {
        return await request<T>(endpoint, opts);
    }
    catch (error) {
        if (error instanceof ApiError && error.status === 401 && !opts._retry) {
            try {
                const data = await api.post<{ access_token: string }>("/auth/refresh");
                useAuthStore.getState().setAccessToken(data.access_token);
                return await request<T>(endpoint, { ...opts, _retry: true });
            }
            catch {
                useAuthStore.getState().logout();
                if (typeof window !== "undefined") {
                    window.location.href = "/login";
                }
                throw error;
            }
        }
        throw error;
    }
}

export const apiAuth = {
    get: async <T>(endpoint: string, options?: ApiRequestInit) =>
        authRequest<T>(endpoint, { ...options, method: "GET" }),

    post: async <T>(endpoint: string, body?: unknown, options?: ApiRequestInit) =>
        authRequest<T>(endpoint, {
            ...options,
            method: "POST",
            body: buildBody(body),
        }),

    patch: async <T>(
        endpoint: string,
        body?: unknown,
        options?: ApiRequestInit,
    ) =>
        authRequest<T>(endpoint, {
            ...options,
            method: "PATCH",
            body: buildBody(body),
        }),

    delete: async <T>(endpoint: string, options?: ApiRequestInit) =>
        authRequest<T>(endpoint, { ...options, method: "DELETE" }),
};
