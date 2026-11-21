import type {Offer} from "../types/offer.ts";
import {apiClient} from "./client.ts";

export const loginUser = async (username: string,password: string): Promise<void> => {
    const response = await apiClient.post('token/', {username, password});
    localStorage.setItem('access_token', response.data.access);
};

export const fetchOffers = async (): Promise<Offer[]> => {
    const response = await apiClient.get<Offer[]>('offers/');
    return response.data;
}