import type { ApiRequestInit } from "./types";
import { API_URL } from "@/shared/config/env";
import { ApiError } from "./types";

let accessToken: string | null = null;

export function setAccessToken(token: string | null) {
    accessToken = token;
}

export function getAccessToken() {
    return accessToken;
}

function buildBody(body: unknown): BodyInit | undefined {
    if (body === undefined || body === null)
        return undefined;
    if (body instanceof FormData)
        return body;
    return JSON.stringify(body);
}

function buildHeaders(body: unknown, extra?: HeadersInit): Record<string, string> {
    const headers: Record<string, string> = {
        ...(extra as Record<string, string>),
    };
    if (!(body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }
    if (accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return headers;
}

export async function request<T>(endpoint: string, options: ApiRequestInit = {}): Promise<T> {
    const { headers: optHeaders, ...rest } = options;

    const response = await fetch(`${API_URL}${endpoint}`, {
        credentials: "include",
        ...rest,
        headers: buildHeaders(rest.body, optHeaders),
    });

    if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new ApiError(response.status, response.statusText, data);
    }

    if (response.status === 204) {
        return undefined as T;
    }

    return response.json() as Promise<T>;
}

export { buildBody };
