export interface IAuthState {
    accessToken: string | null;
    setAccessToken: (token: string | null) => void;
    logout: () => void;
}
