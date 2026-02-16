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
    RefreshCw
} from 'lucide-react';
import api from '../../services/api';
import Loader from '../UI/Loader';

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

    const formatDisplayDate = (dateString) => {
        const date = new Date(dateString);
        const now = new Date();

        // Reset hours to compare calendar days
        const dateCalendar = new Date(date.getFullYear(), date.getMonth(), date.getDate());
        const nowCalendar = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const diffInDays = Math.floor((nowCalendar - dateCalendar) / (1000 * 60 * 60 * 24));

        if (diffInDays === 0) return 'Today';
        if (diffInDays === 1) return 'Yesterday';
        if (diffInDays < 7 && diffInDays > 0) return `${diffInDays} days ago`;

        return new Intl.DateTimeFormat(undefined, {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(date);
    };

    if (loading) {
        return <Loader fullScreen />;
    }

    return (
        <div className="min-h-screen bg-[var(--color-bg-primary)] p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
                            Welcome back, {user?.first_name || 'User'}!
                        </h1>
                        <p className="text-[var(--color-text-secondary)] mt-1">Here's your financial overview</p>
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
                    <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6 flex items-center">
                        <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
                        <span className="text-red-700 dark:text-red-400">{error}</span>
                    </div>
                )}

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {/* Balance Card */}
                    <div className="bg-[var(--color-surface)] rounded-xl p-6 shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-blue-100 dark:bg-blue-900/50 rounded-lg">
                                <Wallet className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                            </div>
                            <span className="text-sm text-[var(--color-text-muted)]">Balance</span>
                        </div>
                        <div className="text-2xl font-bold text-[var(--color-text-primary)]">
                            ${parseFloat(user?.balance || 0).toFixed(2)}
                        </div>
                        <p className="text-sm text-[var(--color-text-muted)] mt-1">Available funds</p>
                    </div>

                    {/* Total Income Card */}
                    <div className="bg-[var(--color-surface)] rounded-xl p-6 shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-green-100 dark:bg-green-900/50 rounded-lg">
                                <TrendingUp className="h-6 w-6 text-green-600 dark:text-green-400" />
                            </div>
                            <span className="text-sm text-[var(--color-text-muted)]">Income</span>
                        </div>
                        <div className="text-2xl font-bold text-[var(--color-text-primary)]">
                            ${calculateTotalIncome().toFixed(2)}
                        </div>
                        <p className="text-sm text-green-600 dark:text-green-400 mt-1 flex items-center">
                            <ArrowUpRight className="h-4 w-4 mr-1" />
                            {incomes.length} transaction{incomes.length !== 1 ? 's' : ''}
                        </p>
                    </div>

                    {/* Total Expenses Card */}
                    <div className="bg-[var(--color-surface)] rounded-xl p-6 shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-red-100 dark:bg-red-900/50 rounded-lg">
                                <TrendingDown className="h-6 w-6 text-red-600 dark:text-red-400" />
                            </div>
                            <span className="text-sm text-[var(--color-text-muted)]">Expenses</span>
                        </div>
                        <div className="text-2xl font-bold text-[var(--color-text-primary)]">
                            ${totalExpenses.toFixed(2)}
                        </div>
                        <p className="text-sm text-red-600 dark:text-red-400 mt-1 flex items-center">
                            <ArrowDownRight className="h-4 w-4 mr-1" />
                            {expenses.length} transaction{expenses.length !== 1 ? 's' : ''}
                        </p>
                    </div>

                    {/* Total Savings Card */}
                    <div className="bg-[var(--color-surface)] rounded-xl p-6 shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center justify-between mb-4">
                            <div className="p-2 bg-purple-100 dark:bg-purple-900/50 rounded-lg">
                                <PiggyBank className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                            </div>
                            <span className="text-sm text-[var(--color-text-muted)]">Savings</span>
                        </div>
                        <div className="text-2xl font-bold text-[var(--color-text-primary)]">
                            ${calculateTotalSavings().toFixed(2)}
                        </div>
                        <p className="text-sm text-purple-600 dark:text-purple-400 mt-1">
                            {savings.length} goal{savings.length !== 1 ? 's' : ''}
                        </p>
                    </div>
                </div>

                {/* Recent Transactions */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                    {/* Recent Income */}
                    <div className="bg-[var(--color-surface)] rounded-xl p-6 shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-semibold text-[var(--color-text-primary)]">Recent Income</h2>
                            <button className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 text-sm font-medium transition-colors">
                                View All
                            </button>
                        </div>
                        <div className="space-y-4">
                            {incomes.length === 0 ? (
                                <div className="text-center py-8">
                                    <TrendingUp className="h-12 w-12 text-[var(--color-text-muted)] mx-auto mb-4 opacity-40" />
                                    <p className="text-[var(--color-text-secondary)]">No income records yet</p>
                                    <p className="text-sm text-[var(--color-text-muted)] mt-1">Add your first income entry to get started</p>
                                </div>
                            ) : (
                                incomes.slice(0, 5).map((income) => (
                                    <div key={income.id} className="flex items-center justify-between">
                                        <div className="flex items-center space-x-3">
                                            <div className="p-2 bg-green-100 dark:bg-green-900/50 rounded-lg">
                                                <ArrowUpRight className="h-4 w-4 text-green-600 dark:text-green-400" />
                                            </div>
                                            <div>
                                                <p className="font-medium text-[var(--color-text-primary)]">{income.source || 'Income'}</p>
                                                <p className="text-sm text-[var(--color-text-muted)]">
                                                    {formatDisplayDate(income.date)}
                                                </p>
                                            </div>
                                        </div>
                                        <span className="font-semibold text-green-600 dark:text-green-400">
                                            +${parseFloat(income.amount || 0).toFixed(2)}
                                        </span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    {/* Recent Expenses */}
                    <div className="bg-[var(--color-surface)] rounded-xl p-6 shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-xl font-semibold text-[var(--color-text-primary)]">Recent Expenses</h2>
                            <button className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 text-sm font-medium transition-colors">
                                View All
                            </button>
                        </div>
                        <div className="space-y-4">
                            {expenses.length === 0 ? (
                                <div className="text-center py-8">
                                    <TrendingDown className="h-12 w-12 text-[var(--color-text-muted)] mx-auto mb-4 opacity-40" />
                                    <p className="text-[var(--color-text-secondary)]">No expense records yet</p>
                                    <p className="text-sm text-[var(--color-text-muted)] mt-1">Track your spending to see insights here</p>
                                </div>
                            ) : (
                                expenses.slice(0, 5).map((expense) => (
                                    <div key={expense.id} className="flex items-center justify-between">
                                        <div className="flex items-center space-x-3">
                                            <div className="p-2 bg-red-100 dark:bg-red-900/50 rounded-lg">
                                                <ArrowDownRight className="h-4 w-4 text-red-600 dark:text-red-400" />
                                            </div>
                                            <div>
                                                <p className="font-medium text-[var(--color-text-primary)]">{expense.category || 'Expense'}</p>
                                                <p className="text-sm text-[var(--color-text-muted)]">
                                                    {formatDisplayDate(expense.date)}
                                                </p>
                                            </div>
                                        </div>
                                        <span className="font-semibold text-red-600 dark:text-red-400">
                                            -${parseFloat(expense.amount || 0).toFixed(2)}
                                        </span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>

                {/* Savings Goals */}
                <div className="bg-[var(--color-surface)] rounded-xl p-6 shadow-sm border border-[var(--color-border)]">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-semibold text-[var(--color-text-primary)]">Savings Goals</h2>
                        <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                            <Plus className="h-4 w-4" />
                            <span>New Goal</span>
                        </button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {savings.length === 0 ? (
                            <div className="col-span-full text-center py-8">
                                <PiggyBank className="h-12 w-12 text-[var(--color-text-muted)] mx-auto mb-4 opacity-40" />
                                <p className="text-[var(--color-text-secondary)]">No savings goals yet</p>
                                <p className="text-sm text-[var(--color-text-muted)] mt-1">Create your first savings goal to start tracking progress</p>
                            </div>
                        ) : (
                            savings.map((saving) => {
                                const currentAmount = parseFloat(saving.current_amount || 0);
                                const goalAmount = parseFloat(saving.goal || saving.amount || 0);
                                const progress = goalAmount > 0 ? Math.min((currentAmount / goalAmount) * 100, 100) : 0;

                                return (
                                    <div key={saving.id} className="border border-[var(--color-border)] rounded-lg p-4 hover:shadow-md transition-shadow bg-[var(--color-bg-secondary)]">
                                        <div className="flex items-center justify-between mb-3">
                                            <h3 className="font-semibold text-[var(--color-text-primary)]">
                                                {saving.description || 'Savings Goal'}
                                            </h3>
                                            {saving.is_completed && (
                                                <span className="text-xs bg-green-100 dark:bg-green-900/50 text-green-600 dark:text-green-400 px-2 py-1 rounded">
                                                    Completed
                                                </span>
                                            )}
                                        </div>
                                        <div className="space-y-2">
                                            <div className="flex justify-between text-sm">
                                                <span className="text-[var(--color-text-secondary)]">Current</span>
                                                <span className="font-medium text-[var(--color-text-primary)]">
                                                    ${currentAmount.toFixed(2)}
                                                </span>
                                            </div>
                                            <div className="flex justify-between text-sm">
                                                <span className="text-[var(--color-text-secondary)]">Goal</span>
                                                <span className="font-medium text-[var(--color-text-primary)]">
                                                    ${goalAmount.toFixed(2)}
                                                </span>
                                            </div>
                                            <div className="w-full bg-[var(--color-bg-hover)] rounded-full h-2">
                                                <div
                                                    className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                                                    style={{ width: `${progress}%` }}
                                                />
                                            </div>
                                            <p className="text-xs text-[var(--color-text-muted)] text-center">
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