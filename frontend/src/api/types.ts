export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_joined: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RegisterResponse {
  user: User;
  tokens: AuthTokens;
  message: string;
}

export interface Category {
  id: number;
  name: string;
  description: string;
}

export interface Expense {
  id: number;
  amount: string;
  description: string;
  notes: string;
  date: string;
  category: number | null;
  category_name: string | null;
  ai_suggested_category: string | null;
  ai_confidence: number | null;
  created_at: string;
  updated_at: string;
}

export interface ExpenseCreate {
  amount: string;
  description: string;
  notes?: string;
  date: string;
  category?: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface QueryResponse {
  query: string;
  response: string;
}
