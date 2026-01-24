// src/services/api.js
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
    constructor() {
        this.token = localStorage.getItem('token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('token');
    }

    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...(this.token && { Authorization: `Bearer ${this.token}` }),
            ...options.headers,
        };

        const config = {
            ...options,
            headers,
        };

        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Something went wrong');
        }

        return data;
    }

    // Auth endpoints
    async login(email, password) {
        const response = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        });
        this.setToken(response.access_token);
        return response;
    }

    async signup(userData) {
        return this.request('/auth/signup', {
            method: 'POST',
            body: JSON.stringify(userData),
        });
    }

    async getCurrentUser() {
        return this.request('/auth/me');
    }

    // User endpoints
    async getUserProfile() {
        return this.request('/users/');
    }

    async updateUserProfile(userData) {
        return this.request('/users/', {
            method: 'PUT',
            body: JSON.stringify(userData),
        });
    }

    // Income endpoints
    async getIncomes(skip = 0, limit = 100) {
        return this.request(`/incomes/?skip=${skip}&limit=${limit}`);
    }

    async getIncome(id) {
        return this.request(`/incomes/${id}`);
    }

    async createIncome(incomeData) {
        return this.request('/incomes/', {
            method: 'POST',
            body: JSON.stringify(incomeData),
        });
    }

    async updateIncome(id, incomeData) {
        return this.request(`/incomes/${id}`, {
            method: 'PUT',
            body: JSON.stringify(incomeData),
        });
    }

    async deleteIncome(id) {
        return this.request(`/incomes/${id}`, {
            method: 'DELETE',
        });
    }

    // Expense endpoints
    async getExpenses(skip = 0, limit = 100) {
        return this.request(`/expenses/?skip=${skip}&limit=${limit}`);
    }

    async getExpense(id) {
        return this.request(`/expenses/${id}`);
    }

    async createExpense(expenseData) {
        return this.request('/expenses/', {
            method: 'POST',
            body: JSON.stringify(expenseData),
        });
    }

    async updateExpense(id, expenseData) {
        return this.request(`/expenses/${id}`, {
            method: 'PUT',
            body: JSON.stringify(expenseData),
        });
    }

    async deleteExpense(id) {
        return this.request(`/expenses/${id}`, {
            method: 'DELETE',
        });
    }

    async getTotalExpenses() {
        return this.request('/expenses/total');
    }

    async getExpensesByCategory(category) {
        return this.request(`/expenses/category/${category}`);
    }

    // Savings endpoints
    async getSavings() {
        return this.request('/savings/');
    }

    async getSaving(id) {
        return this.request(`/savings/${id}`);
    }

    async createSaving(savingData) {
        return this.request('/savings/', {
            method: 'POST',
            body: JSON.stringify(savingData),
        });
    }

    async updateSaving(id, savingData) {
        return this.request(`/savings/${id}`, {
            method: 'PUT',
            body: JSON.stringify(savingData),
        });
    }

    async deleteSaving(id) {
        return this.request(`/savings/${id}`, {
            method: 'DELETE',
        });
    }

    // Admin endpoints
    async getAdminDashboard() {
        return this.request('/admin/dashboard');
    }

    async getAllUsers(skip = 0, limit = 100) {
        return this.request(`/admin/users?skip=${skip}&limit=${limit}`);
    }

    async getUserById(userId) {
        return this.request(`/admin/users/${userId}`);
    }

    async updateUserById(userId, userData) {
        return this.request(`/admin/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData),
        });
    }

    async deleteUserById(userId) {
        return this.request(`/admin/users/${userId}`, {
            method: 'DELETE',
        });
    }

    async activateDeactivateUser(userId, activate) {
        return this.request(`/admin/users/${userId}`, {
            method: 'POST',
            body: JSON.stringify({ activate }),
        });
    }

    async getSavingsSummary(userId = null) {
        const query = userId ? `?user_id=${userId}` : '';
        return this.request(`/admin/savings-summary${query}`);
    }

    async getIncomeSummary(userId = null) {
        const query = userId ? `?user_id=${userId}` : '';
        return this.request(`/admin/income-summary${query}`);
    }

    async getExpensesSummary(userId = null) {
        const query = userId ? `?user_id=${userId}` : '';
        return this.request(`/admin/expenses-summary${query}`);
    }
}

export default new ApiService();