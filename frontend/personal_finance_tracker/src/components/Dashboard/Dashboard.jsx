// src/components/Dashboard/Dashboard.jsx
import { useState, useEffect } from 'react';
import {
    Wallet,
    TrendingUp,
    TrendingDown,
    PiggyBank,
    Plus,
    ArrowUpRight,
    ArrowDownRight
} from 'lucide-react';
import api from '../../services/api';

export default function Dashboard() {
    const [user, setUser] = useState(null);
    const [incomes, setIncomes] = useState([]);
    const [expenses, setExpenses] = useState([]);
    const [savings, setSavings] = useState([]);
    const [totalExpenses, setTotalExpenses] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDashboardData();
    }, []);

    const loadDashboardData = async () => {
        try {
            const [userData, incomesData, expensesData, savingsData, totalExp] = await Promise.all([
                api.getUserProfile(),
                api.getIncomes(),
                api.getExpenses(),
                api.getSavings(),
                api.getTotalExpenses()
            ]);

            setUser(userData.data);
            setIncomes(incomesData.data);
            setExpenses(expensesData.data);
            setSavings(savingsData.data);
            setTotalExpenses(totalExp.total_expenses);
        } catch (error) {
            console.error('Error loading dashboard:', error);
        } finally {
            setLoading(false);
        }
    };

    const calculateTotalIncome = () => {
        return incomes.reduce((sum, income) => sum + parseFloat(income.amount), 0);
    };

    const calculateTotalSavings = () => {
        return savings.reduce((sum, saving) => sum + parseFloat(saving.amount), 0);
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-xl">Loading...</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">
                        Welcome back, {user?.first_name}!
                    </h1>
                    <p className="text-gray-600 mt-1">Here's your financial overview</p>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {/* Balance Card */}
                    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-blue-100 rounded-lg">
                                <Wallet className="h-6 w-6 text-blue-600" />
                            </div>
                            <span className="text-sm text-gray-500">Balance</span>
                        </div>
                        <div className="text-2xl font-bold text-gray-900">
                            ${parseFloat(user?.balance || 0).toFixed(2)}
                        </div>
                        <p className="text-sm text-gray-500 mt-1">Available funds</p>
                    </div>

                    {/* Total Income Card */}
                    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-green-100 rounded-lg">
                                <TrendingUp className="h-6 w-6 text-green-600" />
                            </div>
                            <span className="text-sm text-gray-500">Income</span>
                        </div>
                        <div className="text-2xl font-bold text-gray-900">
                            ${calculateTotalIncome().toFixed(2)}
                        </div>
                        <p className="text-sm text-green-600 mt-1 flex items-center">
                            <ArrowUpRight className="h-4 w-4 mr-1" />
                            {incomes.length} transactions
                        </p>
                    </div>

                    {/* Total Expenses Card */}
                    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-red-100 rounded-lg">
                                <TrendingDown className="h-6 w-6 text-red-600" />
                            </div>
                            <span className="text-sm text-gray-500">Expenses</span>
                        </div>
                        <div className="text-2xl font-bold text-gray-900">
                            ${totalExpenses.toFixed(2)}
                        </div>
                        <p className="text-sm text-red-600 mt-1 flex items-center">
                            <ArrowDownRight className="h-4 w-4 mr-1" />
                            {expenses.length} transactions
                        </p>
                    </div>

                    {/* Total Savings Card */}
                    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-purple-100 rounded-lg">
                                <PiggyBank className="h-6 w-6 text-purple-600" />
                            </div>
                            <span className="text-sm text-gray-500">Savings</span>
                        </div>
                        <div className="text-2xl font-bold text-gray-900">
                            ${calculateTotalSavings().toFixed(2)}
                        </div>
                        <p className="text-sm text-purple-600 mt-1">
                            {savings.length} goals
                        </p>
                    </div>
                </div>

                {/* Recent Transactions */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Recent Income */}
                    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-semibold text-gray-900">Recent Income</h2>
                            <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                                View All
                            </button>
                        </div>
                        <div className="space-y-4">
                            {incomes.slice(0, 5).map((income) => (
                                <div key={income.id} className="flex items-center justify-between">
                                    <div className="flex items-center space-x-3">
                                        <div className="p-2 bg-green-100 rounded-lg">
                                            <ArrowUpRight className="h-4 w-4 text-green-600" />
                                        </div>
                                        <div>
                                            <p className="font-medium text-gray-900">{income.source}</p>
                                            <p className="text-sm text-gray-500">
                                                {new Date(income.date).toLocaleDateString()}
                                            </p>
                                        </div>
                                    </div>
                                    <span className="font-semibold text-green-600">
                                        +${parseFloat(income.amount).toFixed(2)}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Recent Expenses */}
                    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-semibold text-gray-900">Recent Expenses</h2>
                            <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                                View All
                            </button>
                        </div>
                        <div className="space-y-4">
                            {expenses.slice(0, 5).map((expense) => (
                                <div key={expense.id} className="flex items-center justify-between">
                                    <div className="flex items-center space-x-3">
                                        <div className="p-2 bg-red-100 rounded-lg">
                                            <ArrowDownRight className="h-4 w-4 text-red-600" />
                                        </div>
                                        <div>
                                            <p className="font-medium text-gray-900">{expense.category}</p>
                                            <p className="text-sm text-gray-500">
                                                {new Date(expense.date).toLocaleDateString()}
                                            </p>
                                        </div>
                                    </div>
                                    <span className="font-semibold text-red-600">
                                        -${parseFloat(expense.amount).toFixed(2)}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Savings Goals */}
                <div className="mt-6 bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-semibold text-gray-900">Savings Goals</h2>
                        <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                            <Plus className="h-4 w-4" />
                            <span>New Goal</span>
                        </button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {savings.map((saving) => (
                            <div key={saving.id} className="border border-gray-200 rounded-lg p-4">
                                <div className="flex items-center justify-between mb-3">
                                    <h3 className="font-semibold text-gray-900">
                                        {saving.description || 'Savings Goal'}
                                    </h3>
                                    {saving.is_completed && (
                                        <span className="text-xs bg-green-100 text-green-600 px-2 py-1 rounded">
                                            Completed
                                        </span>
                                    )}
                                </div>
                                <div className="space-y-2">
                                    <div className="flex justify-between text-sm">
                                        <span className="text-gray-600">Current</span>
                                        <span className="font-medium">
                                            ${parseFloat(saving.current_amount || 0).toFixed(2)}
                                        </span>
                                    </div>
                                    <div className="flex justify-between text-sm">
                                        <span className="text-gray-600">Goal</span>
                                        <span className="font-medium">
                                            ${parseFloat(saving.goal || saving.amount).toFixed(2)}
                                        </span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className="bg-purple-600 h-2 rounded-full"
                                            style={{
                                                width: `${Math.min(
                                                    (parseFloat(saving.current_amount || 0) /
                                                        parseFloat(saving.goal || saving.amount)) * 100,
                                                    100
                                                )}%`,
                                            }}
                                        />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}