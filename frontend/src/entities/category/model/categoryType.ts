export interface ICategory {
    id: number;
    name: string;
    description: string;
    image_url: string;
    parent_id: number | null;
    sort_order: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface CategoryCardProps {
    category: ICategory;
}
