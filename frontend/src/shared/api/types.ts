export interface ApiRequestInit extends RequestInit {
    _retry?: boolean;
}

export class ApiError extends Error {
    constructor(public status: number, public statusText: string, public data: unknown) {
        super(`${status} ${statusText}`);
    }
}
