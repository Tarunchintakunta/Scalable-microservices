/**
 * TypeScript type definitions
 */

// User & Auth
export interface User {
  id: number;
  email: string;
  full_name?: string;
  role: 'admin' | 'customer';
  created_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  email: string;
  password: string;
  full_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Address
export interface Address {
  id: number;
  user_id: number;
  address_type: 'billing' | 'shipping' | 'both';
  street: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  is_default: boolean;
}

export interface AddressCreate {
  address_type?: string;
  street: string;
  city: string;
  state: string;
  postal_code: string;
  country?: string;
  is_default?: boolean;
}

// Product & Catalog
export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  image_url?: string;
  created_at: string;
}

export interface ProductImage {
  id: number;
  url: string;
  alt_text?: string;
  is_primary: boolean;
  display_order: number;
}

export interface Variant {
  id: number;
  sku: string;
  name: string;
  price: number;
  weight: number;
  attributes?: string;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description?: string;
  base_price: number;
  category_id: number;
  is_active: boolean;
  featured: boolean;
  created_at: string;
  updated_at: string;
  images: ProductImage[];
  variants: Variant[];
}

export interface ProductListItem {
  id: number;
  name: string;
  slug: string;
  base_price: number;
  featured: boolean;
  category_id: number;
  primary_image?: string;
}

// Cart
export interface CartItem {
  id: number;
  cart_id: number;
  product_id: number;
  variant_id?: number;
  sku: string;
  quantity: number;
  price: number;
}

export interface Cart {
  id: number;
  user_id?: number;
  session_id?: string;
  items: CartItem[];
  created_at: string;
  updated_at: string;
}

export interface AddToCartRequest {
  product_id: number;
  variant_id?: number;
  sku: string;
  quantity: number;
}

// Order
export interface OrderItem {
  id: number;
  product_id: number;
  variant_id?: number;
  sku: string;
  product_name: string;
  quantity: number;
  price: number;
}

export interface Order {
  id: number;
  order_number: string;
  status: 'created' | 'paid' | 'packed' | 'shipped' | 'delivered' | 'cancelled';
  subtotal: number;
  tax: number;
  shipping_cost: number;
  total: number;
  shipping_address: string;
  billing_address: string;
  created_at: string;
  updated_at: string;
  paid_at?: string;
  shipped_at?: string;
  delivered_at?: string;
  items: OrderItem[];
}

export interface CheckoutRequest {
  shipping_address_id: number;
  billing_address_id: number;
}

export interface PaymentIntentResponse {
  client_secret: string;
  order_id: number;
}

// Store
export interface Store {
  id: number;
  name: string;
  address: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  latitude: number;
  longitude: number;
  phone?: string;
  email?: string;
  is_active: boolean;
  distance_km?: number;
}

// Review
export interface Review {
  id: number;
  product_id: number;
  user_id: number;
  rating: number;
  title?: string;
  comment?: string;
  verified_purchase: boolean;
  created_at: string;
}

export interface ReviewCreate {
  product_id: number;
  rating: number;
  title?: string;
  comment?: string;
}
