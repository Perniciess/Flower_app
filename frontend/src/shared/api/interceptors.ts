import type { ApiRequestInit } from "@/shared/types/apiTypes";

function getCsrfToken(): string | undefined {
    if (typeof document === "undefined")
        return undefined;
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

export function withCsrf(options: ApiRequestInit): ApiRequestInit {
    const method = options.method?.toLowerCase();
    if (method !== undefined && !["get", "head", "options"].includes(method)) {
        const csrf = getCsrfToken();
        if (csrf !== undefined) {
            return {
                ...options,
                headers: {
                    ...options.headers,
                    "x-csrftoken": csrf,
                },
            };
        }
    }
    return options;
}
