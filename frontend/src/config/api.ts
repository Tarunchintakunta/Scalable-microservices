/**
 * API Configuration
 */

export const API_CONFIG = {
  SERVICE_A_URL: import.meta.env.VITE_SERVICE_A_URL || 'http://localhost:8001',
  SERVICE_B_URL: import.meta.env.VITE_SERVICE_B_URL || 'http://localhost:8002',
  STRIPE_PUBLISHABLE_KEY: import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || '',
};

export const API_ENDPOINTS = {
  // Service A - Auth
  AUTH_SIGNUP: '/auth/signup',
  AUTH_LOGIN: '/auth/login',
  AUTH_ME: '/auth/me',
  
  // Service A - Addresses
  ADDRESSES: '/addresses',
  
  // Service A - Cart
  CART: '/cart',
  CART_ITEMS: '/cart/items',
  
  // Service A - Checkout
  CHECKOUT_PAYMENT_INTENT: '/checkout/create-payment-intent',
  CHECKOUT_CONFIRM: '/checkout/confirm',
  
  // Service A - Orders
  ORDERS: '/orders',
  
  // Service B - Catalog
  CATEGORIES: '/catalog/categories',
  PRODUCTS: '/catalog/products',
  SEARCH: '/catalog/search',
  
  // Service B - Stores
  STORES: '/stores',
  STORES_NEARBY: '/stores/nearby',
  
  // Service B - Reviews
  REVIEWS: '/reviews',
  
  // Service B - Inventory
  INVENTORY: '/inventory',
};
