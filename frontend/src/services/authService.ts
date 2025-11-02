/**
 * Authentication Service
 */
import { serviceA } from '../lib/api-client';
import { API_ENDPOINTS } from '../config/api';
import { LoginCredentials, SignupData, AuthResponse, User } from '../types';

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await serviceA.post<AuthResponse>(
      API_ENDPOINTS.AUTH_LOGIN,
      credentials
    );
    return response.data;
  },

  async signup(data: SignupData): Promise<AuthResponse> {
    const response = await serviceA.post<AuthResponse>(
      API_ENDPOINTS.AUTH_SIGNUP,
      data
    );
    return response.data;
  },

  async getMe(): Promise<User> {
    const response = await serviceA.get<User>(API_ENDPOINTS.AUTH_ME);
    return response.data;
  },
};
