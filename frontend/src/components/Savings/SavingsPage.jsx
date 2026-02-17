import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import Loader from '../UI/Loader';
import { Plus, PiggyBank, RefreshCw, Pencil, Trash2, Calendar, Target, Wallet } from 'lucide-react';
import { useCurrency } from '../../context/CurrencyContext';

const SavingsPage = () => {
    const [savings, setSavings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const { formatCurrency } = useCurrency();
    const [formData, setFormData] = useState({ goal: '', amount: '' });
    const [formError, setFormError] = useState('');
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => { fetchSavings(); }, []);

    const fetchSavings = async () => {
        try {
            setError('');
            const response = await api.getSavings();
            setSavings(response.data || []);
        } catch (error) {
            setError('Failed to load savings. Please try again.');
        } finally { setLoading(false); }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        if (formError) setFormError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormError('');
        setSubmitting(true);
        if (!formData.amount || parseFloat(formData.amount) <= 0) {
            setFormError('Please enter a valid amount greater than 0');
            setSubmitting(false);
            return;
        }
        if (!formData.goal.trim()) {
            setFormError('Please enter a savings goal');
            setSubmitting(false);
            return;
        }
        try {
            await api.createSaving({ ...formData, amount: parseFloat(formData.amount) });
            setFormData({ goal: '', amount: '' });
            fetchSavings();
        } catch (error) {
            setFormError(error.message || 'Failed to create savings goal.');
        } finally { setSubmitting(false); }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this savings goal?')) return;
        try {
            await api.deleteSaving(id);
            fetchSavings();
        } catch (error) {
            setError('Failed to delete savings goal.');
        }
    };

    // Removed local formatCurrency as it's now provided by CurrencyContext

    const inputCls = "w-full p-4 border border-[var(--color-input-border)] rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] outline-none transition-all";

    if (loading) return <Loader />;

    return (
        <div className="space-y-8 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-black text-[var(--color-text-primary)] tracking-tight">Savings Management</h1>
                    <p className="text-sm font-bold text-[var(--color-text-secondary)] mt-1 uppercase tracking-widest opacity-60">Set goals and watch your wealth grow</p>
                </div>
                <button
                    onClick={fetchSavings}
                    className="p-3 bg-[var(--color-bg-hover)] text-[var(--color-text-secondary)] rounded-xl hover:bg-[var(--color-border)] transition-all active:scale-95"
                >
                    <RefreshCw className="h-5 w-5" />
                </button>
            </div>

            {error && (
                <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-sm font-bold text-red-700 dark:text-red-400 px-4 py-3 rounded-xl">
                    {error}
                </div>
            )}

            {/* Add Savings Form */}
            <div className="bg-[var(--color-surface)] rounded-2xl shadow-sm border border-[var(--color-border)] p-8 animate-fade-in stagger-1">
                <h2 className="text-lg font-black mb-6 text-[var(--color-text-primary)] uppercase tracking-widest opacity-80">Define New Goal</h2>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {formError && (
                        <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-xs font-bold text-red-700 dark:text-red-400 px-3 py-2 rounded-lg">
                            {formError}
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label htmlFor="goal" className="block text-xs font-black text-[var(--color-text-secondary)] uppercase tracking-widest mb-2 opacity-60">
                                Goal Description
                            </label>
                            <input
                                type="text"
                                id="goal"
                                name="goal"
                                value={formData.goal}
                                onChange={handleInputChange}
                                placeholder="E.g. Emergency Fund"
                                className={inputCls}
                                required
                                disabled={submitting}
                            />
                        </div>

                        <div>
                            <label htmlFor="amount" className="block text-xs font-black text-[var(--color-text-secondary)] uppercase tracking-widest mb-2 opacity-60">
                                Target Amount
                            </label>
                            <input
                                type="number"
                                id="amount"
                                name="amount"
                                value={formData.amount}
                                onChange={handleInputChange}
                                placeholder="0.00"
                                step="0.01"
                                min="0"
                                className={inputCls}
                                required
                                disabled={submitting}
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={submitting}
                        className="w-full md:w-auto px-8 py-4 bg-indigo-600 text-white text-xs font-black uppercase tracking-widest rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-95"
                    >
                        {submitting ? 'Processing...' : 'Create Savings Goal'}
                    </button>
                </form>
            </div>

            {/* Savings List */}
            <div className="bg-[var(--color-surface)] rounded-2xl shadow-sm border border-[var(--color-border)] overflow-hidden animate-fade-in stagger-2">
                <div className="px-8 py-6 border-b border-[var(--color-border)]">
                    <h2 className="text-lg font-black text-[var(--color-text-primary)] uppercase tracking-widest opacity-80">Financial Targets</h2>
                </div>

                {savings.length === 0 ? (
                    <div className="text-center py-16">
                        <div className="inline-flex p-6 bg-[var(--color-bg-hover)] rounded-3xl mb-4">
                            <PiggyBank className="h-10 w-10 text-[var(--color-text-muted)] opacity-30" />
                        </div>
                        <h3 className="text-sm font-black text-[var(--color-text-primary)] uppercase tracking-widest mb-1">No goals active</h3>
                        <p className="text-xs font-bold text-[var(--color-text-secondary)] opacity-60">Set your first goal to start tracking progress.</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="bg-[var(--color-table-header)] border-b border-[var(--color-border)]">
                                    <th className="px-8 py-4 text-left text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Goal</th>
                                    <th className="px-8 py-4 text-left text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Target</th>
                                    <th className="px-8 py-4 text-left text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Current</th>
                                    <th className="px-8 py-4 text-left text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Progress</th>
                                    <th className="px-8 py-4 text-right text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-[var(--color-table-border)]">
                                {savings.map((saving, index) => {
                                    const progress = saving.current_amount ? (saving.current_amount / saving.amount) * 100 : 0;
                                    return (
                                        <tr key={saving.id} className={`hover:bg-[var(--color-table-hover)] transition-colors animate-fade-in stagger-${index % 5 + 1}`}>
                                            <td className="px-8 py-5 whitespace-nowrap text-sm font-bold text-[var(--color-text-primary)]">
                                                {saving.goal}
                                            </td>
                                            <td className="px-8 py-5 whitespace-nowrap text-sm font-black text-[var(--color-text-secondary)]">
                                                {formatCurrency(saving.amount)}
                                            </td>
                                            <td className="px-8 py-5 whitespace-nowrap text-sm font-black text-indigo-600">
                                                {formatCurrency(saving.current_amount || 0)}
                                            </td>
                                            <td className="px-8 py-5 whitespace-nowrap min-w-48">
                                                <div className="flex items-center gap-3">
                                                    <div className="flex-1 bg-[var(--color-bg-hover)] rounded-full h-1.5 overflow-hidden">
                                                        <div
                                                            className="bg-indigo-600 h-full rounded-full transition-all duration-1000 ease-out"
                                                            style={{ width: `${Math.min(progress, 100)}%` }}
                                                        ></div>
                                                    </div>
                                                    <span className="text-[10px] font-black text-indigo-600 w-8">{progress.toFixed(0)}%</span>
                                                </div>
                                            </td>
                                            <td className="px-8 py-5 whitespace-nowrap text-right">
                                                <button
                                                    onClick={() => handleDelete(saving.id)}
                                                    className="p-2 text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/30 rounded-lg transition-all active:scale-90"
                                                >
                                                    <LogOut className="h-4 w-4 rotate-180" />
                                                </button>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default SavingsPage;