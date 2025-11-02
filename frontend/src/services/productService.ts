/**
 * Product Service
 */
import { serviceB } from '../lib/api-client';
import { API_ENDPOINTS } from '../config/api';
import { Category, Product, ProductListItem } from '../types';

export const productService = {
  async getCategories(): Promise<Category[]> {
    const response = await serviceB.get<Category[]>(API_ENDPOINTS.CATEGORIES);
    return response.data;
  },

  async getProducts(params?: {
    category_id?: number;
    featured?: boolean;
    skip?: number;
    limit?: number;
  }): Promise<ProductListItem[]> {
    const response = await serviceB.get<ProductListItem[]>(
      API_ENDPOINTS.PRODUCTS,
      { params }
    );
    return response.data;
  },

  async getProduct(id: number): Promise<Product> {
    const response = await serviceB.get<Product>(
      `${API_ENDPOINTS.PRODUCTS}/${id}`
    );
    return response.data;
  },

  async searchProducts(query: string): Promise<ProductListItem[]> {
    const response = await serviceB.get<ProductListItem[]>(
      API_ENDPOINTS.SEARCH,
      { params: { q: query } }
    );
    return response.data;
  },
};
