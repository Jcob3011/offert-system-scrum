export interface Company{
    id: number;
    name: string;
    nip: string;
    address: string;
}

export interface OfferItem{
    id?: number;
    description?: string;
    quantity: number;
    price_per_unit: string;
    price_in_eur?: string | null;
    total_price?: string;
}

export interface Seller {
    id: number;
    name: string;
    nip: string;
    address: string;
    email?: string;
    phone?: string;
    bank_account?: string;
    logo?: string | null;
}

export interface Client {
    id: number;
    company: number;
    first_name: string;
    last_name: string;
    email: string;
    phone?: string;
    position?: string;
}

export interface Offer {
    id: number;
    offer_number: string;
    seller: number;
    client: number;
    status: 'draft' | 'pending' | 'consultation' | 'approved' | 'sent' | 'rejected';
    description: string | null;
    total_price: string;
    total_vat: string;
    total_gross: string;
    validity_days: number;
    payment_deadline_days: number;
    payment_method: string;
    rejection_reason?: string | null;
    created_by?: string | null;
    created_at: string;
    valid_until_date: string | null;
    items: OfferItem[];

}