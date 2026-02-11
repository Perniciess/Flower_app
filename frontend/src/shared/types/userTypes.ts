enum Role {
    ADMIN = "admin",
    CLIENT = "client",
}

export interface IUser {
    id: number;
    phone_number: string;
    name: string;
    role: Role;
}
