/**
 * Cart Service
 */
import { serviceA } from '../lib/api-client';
import { API_ENDPOINTS } from '../config/api';
import { Cart, AddToCartRequest } from '../types';

export const cartService = {
  async getCart(): Promise<Cart> {
    const response = await serviceA.get<Cart>(API_ENDPOINTS.CART);
    return response.data;
  },

  async addToCart(item: AddToCartRequest): Promise<Cart> {
    const response = await serviceA.post<Cart>(
      API_ENDPOINTS.CART_ITEMS,
      item
    );
    return response.data;
  },

  async updateCartItem(itemId: number, quantity: number): Promise<Cart> {
    const response = await serviceA.put<Cart>(
      `${API_ENDPOINTS.CART_ITEMS}/${itemId}`,
      { quantity }
    );
    return response.data;
  },

  async removeFromCart(itemId: number): Promise<Cart> {
    const response = await serviceA.delete<Cart>(
      `${API_ENDPOINTS.CART_ITEMS}/${itemId}`
    );
    return response.data;
  },

  async clearCart(): Promise<void> {
    await serviceA.delete(API_ENDPOINTS.CART);
  },
};
