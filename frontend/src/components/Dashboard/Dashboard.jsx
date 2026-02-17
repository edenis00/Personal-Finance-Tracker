// src/components/Dashboard/Dashboard.jsx
import { useState, useEffect } from 'react';
import { Plus, ArrowUpRight, ArrowDownRight, Wallet, TrendingUp, TrendingDown, PiggyBank, RefreshCw } from 'lucide-react';
import { useCurrency } from '../../context/CurrencyContext';
import api from '../../services/api';
import Loader from '../UI/Loader';

export default function Dashboard() {
    const [user, setUser] = useState(null);
    const [incomes, setIncomes] = useState([]);
    const [expenses, setExpenses] = useState([]);
    const [savings, setSavings] = useState([]);
    const [totalExpenses, setTotalExpenses] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const { formatCurrency } = useCurrency();
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
                <div className="flex items-center justify-between mb-8 animate-fade-in">
                    <div>
                        <h1 className="text-3xl font-black text-[var(--color-text-primary)] tracking-tight">
                            Welcome back, <span className="text-indigo-600">{user?.first_name || 'User'}!</span>
                        </h1>
                        <p className="text-[var(--color-text-secondary)] text-sm mt-1">Here's your financial overview</p>
                    </div>
                    <button
                        onClick={handleRefresh}
                        disabled={refreshing}
                        className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                        <span>{refreshing ? 'Updating...' : 'Refresh'}</span>
                    </button>
                </div>

                {error && (
                    <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 rounded-xl p-4 mb-8 flex items-center animate-fade-in">
                        <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
                        <span className="text-sm font-bold text-red-700 dark:text-red-400">{error}</span>
                    </div>
                )}

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
                    {/* Balance Card */}
                    <div className="bg-[var(--color-surface)] rounded-2xl p-6 shadow-sm border border-[var(--color-border)] animate-fade-in stagger-1">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-3 bg-indigo-100 dark:bg-indigo-900/40 rounded-xl">
                                <Wallet className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
                            </div>
                            <span className="text-[10px] font-black uppercase tracking-widest text-[var(--color-text-muted)] opacity-60">Balance</span>
                        </div>
                        <div className="text-xl font-black text-[var(--color-text-primary)] tracking-tight mb-1">
                            {formatCurrency(user?.balance || 0)}
                        </div>
                        <p className="text-[10px] font-bold text-[var(--color-text-muted)] uppercase tracking-widest opacity-50">Available funds</p>
                    </div>

                    {/* Total Income Card */}
                    <div className="bg-[var(--color-surface)] rounded-2xl p-6 shadow-sm border border-[var(--color-border)] animate-fade-in stagger-2">
                        <div className="flex items-center gap-2 mb-6">
                            <div className="p-3 bg-emerald-100 dark:bg-emerald-900/40 rounded-xl">
                                <TrendingUp className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
                            </div>
                            <span className="text-[10px] font-black uppercase tracking-widest text-[var(--color-text-muted)] opacity-60">Income</span>
                        </div>
                        <div className="text-xl font-black text-[var(--color-text-primary)] tracking-tight mb-1">
                            {formatCurrency(calculateTotalIncome())}
                        </div>
                        <p className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-widest flex items-center">
                            <ArrowUpRight className="h-3 w-3 mr-1" />
                            {incomes.length} inflow source{incomes.length !== 1 ? 's' : ''}
                        </p>
                    </div>

                    {/* Total Expenses Card */}
                    <div className="bg-[var(--color-surface)] rounded-2xl p-6 shadow-sm border border-[var(--color-border)] animate-fade-in stagger-3">
                        <div className="flex items-center gap-2 mb-6">
                            <div className="p-3 bg-rose-100 dark:bg-rose-900/40 rounded-xl">
                                <TrendingDown className="h-5 w-5 text-rose-600 dark:text-rose-400" />
                            </div>
                            <span className="text-[10px] font-black uppercase tracking-widest text-[var(--color-text-muted)] opacity-60">Expenses</span>
                        </div>
                        <div className="text-xl font-black text-[var(--color-text-primary)] tracking-tight mb-1">
                            {formatCurrency(totalExpenses)}
                        </div>
                        <p className="text-[10px] font-bold text-rose-600 dark:text-rose-400 uppercase tracking-widest flex items-center">
                            <ArrowDownRight className="h-3 w-3 mr-1" />
                            {expenses.length} outflow event{expenses.length !== 1 ? 's' : ''}
                        </p>
                    </div>

                    {/* Total Savings Card */}
                    <div className="bg-[var(--color-surface)] rounded-2xl p-6 shadow-sm border border-[var(--color-border)] animate-fade-in stagger-4">
                        <div className="flex items-center gap-2 mb-6">
                            <div className="p-3 bg-amber-100 dark:bg-amber-900/40 rounded-xl">
                                <PiggyBank className="h-5 w-5 text-amber-600 dark:text-amber-400" />
                            </div>
                            <span className="text-[10px] font-black uppercase tracking-widest text-[var(--color-text-muted)] opacity-60">Savings</span>
                        </div>
                        <div className="text-xl font-black text-[var(--color-text-primary)] tracking-tight mb-1">
                            {formatCurrency(calculateTotalSavings())}
                        </div>
                        <p className="text-[10px] font-bold text-amber-600 dark:text-amber-400 uppercase tracking-widest">
                            {savings.length} goal{savings.length !== 1 ? 's' : ''} in progress
                        </p>
                    </div>
                </div>

                {/* Recent Transactions */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    {/* Recent Income */}
                    <div className="bg-[var(--color-surface)] rounded-2xl p-6 shadow-sm border border-[var(--color-border)] animate-fade-in stagger-2">
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-xl font-black text-[var(--color-text-primary)] tracking-tight">Recent Income</h2>
                            <button className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 text-[10px] font-black uppercase tracking-widest transition-colors">
                                View History
                            </button>
                        </div>
                        <div className="space-y-6">
                            {incomes.length === 0 ? (
                                <div className="text-center py-10">
                                    <div className="inline-flex p-4 bg-[var(--color-bg-hover)] rounded-2xl mb-4">
                                        <TrendingUp className="h-8 w-8 text-[var(--color-text-muted)] opacity-40" />
                                    </div>
                                    <p className="text-sm font-bold text-[var(--color-text-secondary)]">No income records yet</p>
                                    <p className="text-[10px] font-bold text-[var(--color-text-muted)] mt-1 uppercase tracking-widest opacity-50">Add your first inflow to see insights</p>
                                </div>
                            ) : (
                                incomes.slice(0, 5).map((income, index) => (
                                    <div key={income.id} className={`flex items-center justify-between animate-fade-in stagger-${index + 1}`}>
                                        <div className="flex items-center space-x-4">
                                            <div className="p-2.5 bg-emerald-100/50 dark:bg-emerald-900/30 rounded-xl">
                                                <ArrowUpRight className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
                                            </div>
                                            <div>
                                                <p className="text-sm font-bold text-[var(--color-text-primary)]">{income.source || 'Income Source'}</p>
                                                <p className="text-[10px] font-bold text-[var(--color-text-muted)] uppercase tracking-widest opacity-60">
                                                    {formatDisplayDate(income.date)}
                                                </p>
                                            </div>
                                        </div>
                                        <span className="text-sm font-black text-emerald-600 dark:text-emerald-400">
                                            +{formatCurrency(income.amount || 0)}
                                        </span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    {/* Recent Expenses */}
                    <div className="bg-[var(--color-surface)] rounded-2xl p-6 shadow-sm border border-[var(--color-border)] animate-fade-in stagger-3">
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-xl font-black text-[var(--color-text-primary)] tracking-tight">Recent Expenses</h2>
                            <button className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 text-[10px] font-black uppercase tracking-widest transition-colors">
                                Report Analysis
                            </button>
                        </div>
                        <div className="space-y-6">
                            {expenses.length === 0 ? (
                                <div className="text-center py-10">
                                    <div className="inline-flex p-4 bg-[var(--color-bg-hover)] rounded-2xl mb-4">
                                        <TrendingDown className="h-8 w-8 text-[var(--color-text-muted)] opacity-40" />
                                    </div>
                                    <p className="text-sm font-bold text-[var(--color-text-secondary)]">No expense records yet</p>
                                    <p className="text-[10px] font-bold text-[var(--color-text-muted)] mt-1 uppercase tracking-widest opacity-50">Track your spending to see analysis</p>
                                </div>
                            ) : (
                                expenses.slice(0, 5).map((expense, index) => (
                                    <div key={expense.id} className={`flex items-center justify-between animate-fade-in stagger-${index + 1}`}>
                                        <div className="flex items-center space-x-4">
                                            <div className="p-2.5 bg-rose-100/50 dark:bg-rose-900/30 rounded-xl">
                                                <ArrowDownRight className="h-4 w-4 text-rose-600 dark:text-rose-400" />
                                            </div>
                                            <div>
                                                <p className="text-sm font-bold text-[var(--color-text-primary)]">{expense.category || 'Expense Category'}</p>
                                                <p className="text-[10px] font-bold text-[var(--color-text-muted)] uppercase tracking-widest opacity-60">
                                                    {formatDisplayDate(expense.date)}
                                                </p>
                                            </div>
                                        </div>
                                        <span className="text-sm font-black text-rose-600 dark:text-rose-400">
                                            -{formatCurrency(expense.amount || 0)}
                                        </span>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>

                {/* Savings Goals */}
                <div className="bg-[var(--color-surface)] rounded-2xl p-8 shadow-sm border border-[var(--color-border)] animate-fade-in stagger-4">
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-xl font-black text-[var(--color-text-primary)] tracking-tight">Financial Targets</h2>
                        <button className="flex items-center space-x-2 px-6 py-3 bg-indigo-600 text-white text-[10px] font-black uppercase tracking-widest rounded-xl hover:bg-indigo-700 transition-all active:scale-95">
                            <Plus className="h-3 w-3" />
                            <span>New Strategic Goal</span>
                        </button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {savings.length === 0 ? (
                            <div className="col-span-full text-center py-12">
                                <div className="inline-flex p-5 bg-[var(--color-bg-hover)] rounded-2xl mb-4">
                                    <PiggyBank className="h-10 w-10 text-[var(--color-text-muted)] opacity-30" />
                                </div>
                                <p className="text-sm font-bold text-[var(--color-text-secondary)]">No active targets found</p>
                                <p className="text-[10px] font-bold text-[var(--color-text-muted)] mt-1 uppercase tracking-widest opacity-50">Blueprint your wealth expansion</p>
                            </div>
                        ) : (
                            savings.map((saving, index) => {
                                const currentAmount = parseFloat(saving.current_amount || 0);
                                const targetAmount = parseFloat(saving.amount || 0);
                                const progress = targetAmount > 0 ? Math.min((currentAmount / targetAmount) * 100, 100) : 0;

                                return (
                                    <div key={saving.id} className={`border border-[var(--color-border)] rounded-2xl p-6 hover:shadow-xl hover:shadow-indigo-500/5 transition-all bg-[var(--color-bg-hover)]/30 animate-fade-in stagger-${index + 1}`}>
                                        <div className="flex items-center justify-between mb-6">
                                            <h3 className="text-sm font-black text-[var(--color-text-primary)] uppercase tracking-widest opacity-80">
                                                {saving.goal || 'Wealth Buffer'}
                                            </h3>
                                            {progress >= 100 && (
                                                <span className="text-[10px] font-black uppercase tracking-widest bg-emerald-100 dark:bg-emerald-900/50 text-emerald-600 dark:text-emerald-400 px-2.5 py-1 rounded-lg">
                                                    Target Hit
                                                </span>
                                            )}
                                        </div>
                                        <div className="space-y-4">
                                            <div className="flex justify-between items-end">
                                                <div>
                                                    <p className="text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-widest opacity-50 mb-1">Current</p>
                                                    <p className="text-lg font-black text-indigo-600 tracking-tight">
                                                        {formatCurrency(currentAmount)}
                                                    </p>
                                                </div>
                                                <div className="text-right">
                                                    <p className="text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-widest opacity-50 mb-1">Target</p>
                                                    <p className="text-sm font-bold text-[var(--color-text-primary)] opacity-80">
                                                        {formatCurrency(targetAmount)}
                                                    </p>
                                                </div>
                                            </div>
                                            <div className="space-y-2">
                                                <div className="w-full bg-[var(--color-border)] rounded-full h-1.5 overflow-hidden">
                                                    <div
                                                        className="bg-indigo-600 h-full rounded-full transition-all duration-1000 ease-out"
                                                        style={{ width: `${progress}%` }}
                                                    />
                                                </div>
                                                <p className="text-[10px] font-black text-indigo-600 uppercase tracking-widest text-center opacity-80">
                                                    {progress.toFixed(0)}% Consolidated
                                                </p>
                                            </div>
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