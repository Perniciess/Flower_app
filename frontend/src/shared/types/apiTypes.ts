export interface ApiRequestInit extends RequestInit {
    _retry?: boolean;
}

export class ApiError extends Error {
    constructor(
        public status: number,
        public statusText: string,
        public data: unknown,
    ) {
        super(`${status} ${statusText}`);
    }
}

export interface Page<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
    pages: number;
}
