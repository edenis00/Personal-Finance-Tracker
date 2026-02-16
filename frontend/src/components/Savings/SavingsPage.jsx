import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import Loader from '../UI/Loader';

const SavingsPage = () => {
    const [savings, setSavings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
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
        if (!formData.amount || parseFloat(formData.amount) <= 0) { setFormError('Please enter a valid amount greater than 0'); setSubmitting(false); return; }
        if (!formData.goal.trim()) { setFormError('Please enter a savings goal'); setSubmitting(false); return; }
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
        try { await api.deleteSaving(id); fetchSavings(); } catch (error) { setError('Failed to delete savings goal.'); }
    };

    const inputCls = "w-full p-3 border border-[var(--color-input-border)] rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] outline-none transition-colors";

    if (loading) return <Loader />;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">Savings Management</h1>
                <button onClick={fetchSavings} className="px-4 py-2 bg-[var(--color-bg-hover)] text-[var(--color-text-secondary)] rounded-md hover:bg-[var(--color-border)] transition-colors">Refresh</button>
            </div>
            {error && (<div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-md">{error}</div>)}
            <div className="bg-[var(--color-surface)] rounded-lg shadow-sm border border-[var(--color-border)] p-6">
                <h2 className="text-xl font-semibold mb-4 text-[var(--color-text-primary)]">Add New Savings Goal</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    {formError && (<div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-3 py-2 rounded-md text-sm">{formError}</div>)}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label htmlFor="goal" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">Savings Goal</label>
                            <input type="text" id="goal" name="goal" value={formData.goal} onChange={handleInputChange} placeholder="Emergency Fund, Vacation, etc." className={inputCls} required disabled={submitting} />
                        </div>
                        <div>
                            <label htmlFor="amount" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">Target Amount ($)</label>
                            <input type="number" id="amount" name="amount" value={formData.amount} onChange={handleInputChange} placeholder="0.00" step="0.01" min="0" className={inputCls} required disabled={submitting} />
                        </div>
                    </div>
                    <button type="submit" disabled={submitting} className="w-full md:w-auto px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">{submitting ? 'Adding Goal...' : 'Add Savings Goal'}</button>
                </form>
            </div>
            <div className="bg-[var(--color-surface)] rounded-lg shadow-sm border border-[var(--color-border)] overflow-hidden">
                <div className="px-6 py-4 border-b border-[var(--color-border)]">
                    <h2 className="text-xl font-semibold text-[var(--color-text-primary)]">Your Savings Goals</h2>
                    <p className="text-sm text-[var(--color-text-secondary)] mt-1">Track your progress towards financial goals</p>
                </div>
                {savings.length === 0 ? (
                    <div className="text-center py-12">
                        <div className="text-[var(--color-text-muted)] text-4xl mb-4">🎯</div>
                        <h3 className="text-lg font-medium text-[var(--color-text-primary)] mb-2">No savings goals yet</h3>
                        <p className="text-[var(--color-text-secondary)]">Set your first savings goal above to start building wealth.</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-[var(--color-table-header)]">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Goal</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Target Amount</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Current Amount</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Progress</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-[var(--color-table-border)]">
                                {savings.map(saving => {
                                    const progress = saving.current_amount ? (saving.current_amount / saving.amount) * 100 : 0;
                                    return (
                                        <tr key={saving.id} className="hover:bg-[var(--color-table-hover)] transition-colors">
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-[var(--color-text-primary)]">{saving.goal}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-[var(--color-text-primary)]">${parseFloat(saving.amount).toFixed(2)}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-[var(--color-text-secondary)]">${parseFloat(saving.current_amount || 0).toFixed(2)}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <div className="flex items-center">
                                                    <div className="flex-1 bg-[var(--color-bg-hover)] rounded-full h-2 mr-2">
                                                        <div className="bg-green-600 h-2 rounded-full transition-all duration-300" style={{ width: `${Math.min(progress, 100)}%` }}></div>
                                                    </div>
                                                    <span className="text-sm text-[var(--color-text-secondary)]">{progress.toFixed(0)}%</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                                <button onClick={() => handleDelete(saving.id)} className="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300 px-3 py-1 rounded-md hover:bg-red-50 dark:hover:bg-red-950/50 transition-colors">Delete</button>
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