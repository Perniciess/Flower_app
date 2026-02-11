interface IProductImage {
    id: number;
    url: string;
    sort_order: number;
}

interface IFlowerInComposition {
    id: number;
    name: string;
    price: string;
}

export interface IProduct {
    id: number;
    name: string;
    price: string;
    description: string;
    color: string;
    is_active: boolean;
    in_stock: boolean;
    images: IProductImage[];
    composition: IFlowerInComposition[];
    discounted_price: string | null;
    discount_percentage: string | null;
}

export interface ProductCardProps {
    product: IProduct;
}
