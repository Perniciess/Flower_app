import type { ApiRequestInit } from "./types";
import { buildBody, request } from "./base";
import { withCsrf } from "./interceptors";
import { ApiError } from "./types";

export const api = {
    get: async <T>(endpoint: string, options?: ApiRequestInit) =>
        request<T>(endpoint, { ...options, method: "GET" }),

    post: async <T>(endpoint: string, body?: unknown, options?: ApiRequestInit) =>
        request<T>(endpoint, { ...options, method: "POST", body: buildBody(body) }),

    patch: async <T>(endpoint: string, body?: unknown, options?: ApiRequestInit) =>
        request<T>(endpoint, { ...options, method: "PATCH", body: buildBody(body) }),

    delete: async <T>(endpoint: string, options?: ApiRequestInit) =>
        request<T>(endpoint, { ...options, method: "DELETE" }),
};

async function authRequest<T>(endpoint: string, options: ApiRequestInit = {}): Promise<T> {
    const opts = withCsrf(options);

    try {
        return await request<T>(endpoint, opts);
    }
    catch (error) {
        if (error instanceof ApiError && error.status === 401 && !opts._retry) {
            try {
                await api.post("/auth/refresh");
                return await request<T>(endpoint, { ...opts, _retry: true });
            }
            catch {
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
        authRequest<T>(endpoint, { ...options, method: "POST", body: buildBody(body) }),

    patch: async <T>(endpoint: string, body?: unknown, options?: ApiRequestInit) =>
        authRequest<T>(endpoint, { ...options, method: "PATCH", body: buildBody(body) }),

    delete: async <T>(endpoint: string, options?: ApiRequestInit) =>
        authRequest<T>(endpoint, { ...options, method: "DELETE" }),
};
