// src/components/Dashboard/Dashboard.jsx
import { useState, useEffect } from 'react';
import {
    Wallet,
    TrendingUp,
    TrendingDown,
    PiggyBank,
    Plus,
    ArrowUpRight,
    ArrowDownRight,
    AlertCircle,
    Loader2,
    RefreshCw
} from 'lucide-react';
import api from '../../services/api';

export default function Dashboard() {
    const [user, setUser] = useState(null);
    const [incomes, setIncomes] = useState([]);
    const [expenses, setExpenses] = useState([]);
    const [savings, setSavings] = useState([]);
    const [totalExpenses, setTotalExpenses] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [refreshing, setRefreshing] = useState(false);

    useEffect(() => {
        loadDashboardData();
    }, []);

    const loadDashboardData = async () => {
        try {
            setError(null);
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
            setTotalExpenses(totalExp.total_expenses || 0);
        } catch (error) {
            console.error('Error loading dashboard:', error);
            setError('Failed to load dashboard data. Please try refreshing the page.');
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    const handleRefresh = async () => {
        setRefreshing(true);
        await loadDashboardData();
    };

    const calculateTotalIncome = () => {
        return incomes.reduce((sum, income) => sum + parseFloat(income.amount || 0), 0);
    };

    const calculateTotalSavings = () => {
        return savings.reduce((sum, saving) => sum + parseFloat(saving.current_amount || saving.amount || 0), 0);
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <Loader2 className="h-8 w-8 animate-spin text-blue-500 mx-auto mb-4" />
                    <p className="text-gray-600">Loading your financial overview...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">
                            Welcome back, {user?.first_name || 'User'}!
                        </h1>
                        <p className="text-gray-600 mt-1">Here's your financial overview</p>
                    </div>
                    <button
                        onClick={handleRefresh}
                        disabled={refreshing}
                        className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                        <span>{refreshing ? 'Refreshing...' : 'Refresh'}</span>
                    </button>
                </div>

                {error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-center">
                        <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
                        <span className="text-red-700">{error}</span>
                    </div>
                )}

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
                            {incomes.length} transaction{incomes.length !== 1 ? 's' : ''}
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
                            {expenses.length} transaction{expenses.length !== 1 ? 's' : ''}
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
                            {savings.length} goal{savings.length !== 1 ? 's' : ''}
                        </p>
                    </div>
                </div>

                {/* Recent Transactions */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                    {/* Recent Income */}
                    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-semibold text-gray-900">Recent Income</h2>
                            <button className="text-blue-600 hover:text-blue-700 text-sm font-medium transition-colors">
                                View All
                            </button>
                        </div>
                        <div className="space-y-4">
                            {incomes.length === 0 ? (
                                <div className="text-center py-8">
                                    <TrendingUp className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                                    <p className="text-gray-500">No income records yet</p>
                                    <p className="text-sm text-gray-400 mt-1">Add your first income entry to get started</p>
                                </div>
                            ) : (
                                incomes.slice(0, 5).map((income) => (
                                    <div key={income.id} className="flex items-center justify-between">
                                        <div className="flex items-center space-x-3">
                                            <div className="p-2 bg-green-100 rounded-lg">
                                                <ArrowUpRight className="h-4 w-4 text-green-600" />
                                            </div>
                                            <div>
                                                <p className="font-medium text-gray-900">{income.source || 'Income'}</p>
                                                <p className="text-sm text-gray-500">
                                                    {new Date(income.date).toLocaleDateString()}
                                                </p>
                                            </div>
                                        </div>
                                        <span className="font-semibold text-green-600">
                                            +${parseFloat(income.amount || 0).toFixed(2)}
                                        </span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    {/* Recent Expenses */}
                    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-semibold text-gray-900">Recent Expenses</h2>
                            <button className="text-blue-600 hover:text-blue-700 text-sm font-medium transition-colors">
                                View All
                            </button>
                        </div>
                        <div className="space-y-4">
                            {expenses.length === 0 ? (
                                <div className="text-center py-8">
                                    <TrendingDown className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                                    <p className="text-gray-500">No expense records yet</p>
                                    <p className="text-sm text-gray-400 mt-1">Track your spending to see insights here</p>
                                </div>
                            ) : (
                                expenses.slice(0, 5).map((expense) => (
                                    <div key={expense.id} className="flex items-center justify-between">
                                        <div className="flex items-center space-x-3">
                                            <div className="p-2 bg-red-100 rounded-lg">
                                                <ArrowDownRight className="h-4 w-4 text-red-600" />
                                            </div>
                                            <div>
                                                <p className="font-medium text-gray-900">{expense.category || 'Expense'}</p>
                                                <p className="text-sm text-gray-500">
                                                    {new Date(expense.date).toLocaleDateString()}
                                                </p>
                                            </div>
                                        </div>
                                        <span className="font-semibold text-red-600">
                                            -${parseFloat(expense.amount || 0).toFixed(2)}
                                        </span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>

                {/* Savings Goals */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-semibold text-gray-900">Savings Goals</h2>
                        <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                            <Plus className="h-4 w-4" />
                            <span>New Goal</span>
                        </button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {savings.length === 0 ? (
                            <div className="col-span-full text-center py-8">
                                <PiggyBank className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                                <p className="text-gray-500">No savings goals yet</p>
                                <p className="text-sm text-gray-400 mt-1">Create your first savings goal to start tracking progress</p>
                            </div>
                        ) : (
                            savings.map((saving) => {
                                const currentAmount = parseFloat(saving.current_amount || 0);
                                const goalAmount = parseFloat(saving.goal || saving.amount || 0);
                                const progress = goalAmount > 0 ? Math.min((currentAmount / goalAmount) * 100, 100) : 0;

                                return (
                                    <div key={saving.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
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
                                                    ${currentAmount.toFixed(2)}
                                                </span>
                                            </div>
                                            <div className="flex justify-between text-sm">
                                                <span className="text-gray-600">Goal</span>
                                                <span className="font-medium">
                                                    ${goalAmount.toFixed(2)}
                                                </span>
                                            </div>
                                            <div className="w-full bg-gray-200 rounded-full h-2">
                                                <div
                                                    className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                                                    style={{ width: `${progress}%` }}
                                                />
                                            </div>
                                            <p className="text-xs text-gray-500 text-center">
                                                {progress.toFixed(1)}% complete
                                            </p>
                                        </div>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}