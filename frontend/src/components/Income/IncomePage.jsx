import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import Loader from '../UI/Loader';
import { RefreshCw, LogOut } from 'lucide-react';
import { useCurrency } from '../../context/CurrencyContext';

const IncomePage = () => {
    const [incomes, setIncomes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const { formatCurrency } = useCurrency();
    const [formData, setFormData] = useState({
        amount: '',
        source: '',
        date: new Date().toISOString().split('T')[0]
    });
    const [formError, setFormError] = useState('');
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        fetchIncomes();
    }, []);

    const fetchIncomes = async () => {
        try {
            setError('');
            const response = await api.getIncomes();
            setIncomes(response.data || []);
        } catch (error) {
            console.error('Error fetching incomes:', error);
            setError('Failed to load incomes. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        // Clear form error when user starts typing
        if (formError) setFormError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setFormError('');
        setSubmitting(true);

        // Validation
        if (!formData.amount || parseFloat(formData.amount) <= 0) {
            setFormError('Please enter a valid amount greater than 0');
            setSubmitting(false);
            return;
        }

        if (!formData.description.trim()) {
            setFormError('Please enter a description');
            setSubmitting(false);
            return;
        }

        try {
            await api.createIncome({
                ...formData,
                amount: parseFloat(formData.amount)
            });
            setFormData({
                amount: '',
                description: '',
                date: new Date().toISOString().split('T')[0]
            });
            fetchIncomes(); // Refresh the list
        } catch (error) {
            console.error('Error creating income:', error);
            setFormError(error.message || 'Failed to create income. Please try again.');
        } finally {
            setSubmitting(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this income?')) {
            return;
        }

        try {
            await api.deleteIncome(id);
            fetchIncomes(); // Refresh the list
        } catch (error) {
            console.error('Error deleting income:', error);
            setError('Failed to delete income. Please try again.');
        }
    };

    // Removed local formatCurrency as it's now provided by CurrencyContext

    const inputClasses = "w-full p-4 border border-[var(--color-input-border)] rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] outline-none transition-all";

    if (loading) {
        return <Loader />;
    }

    return (
        <div className="space-y-8 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-black text-[var(--color-text-primary)] tracking-tight">Income Management</h1>
                    <p className="text-sm font-bold text-[var(--color-text-secondary)] mt-1 uppercase tracking-widest opacity-60">Monitor and categorize your revenue</p>
                </div>
                <button
                    onClick={fetchIncomes}
                    className="p-3 bg-[var(--color-bg-hover)] text-[var(--color-text-secondary)] rounded-xl hover:bg-[var(--color-border)] transition-all active:scale-95"
                    title="Refresh Data"
                >
                    <RefreshCw className="h-5 w-5" />
                </button>
            </div>

            {error && (
                <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-sm font-bold text-red-700 dark:text-red-400 px-4 py-3 rounded-xl animate-fade-in">
                    {error}
                </div>
            )}

            {/* Add Income Form */}
            <div className="bg-[var(--color-surface)] rounded-2xl shadow-sm border border-[var(--color-border)] p-8 animate-fade-in stagger-1">
                <h2 className="text-lg font-black mb-6 text-[var(--color-text-primary)] uppercase tracking-widest opacity-80">Record New Income</h2>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {formError && (
                        <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-xs font-bold text-red-700 dark:text-red-400 px-3 py-2 rounded-lg">
                            {formError}
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div>
                            <label htmlFor="amount" className="block text-xs font-black text-[var(--color-text-secondary)] uppercase tracking-widest mb-2 opacity-60">
                                Amount
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
                                className={inputClasses}
                                required
                                disabled={submitting}
                            />
                        </div>

                        <div>
                            <label htmlFor="description" className="block text-xs font-black text-[var(--color-text-secondary)] uppercase tracking-widest mb-2 opacity-60">
                                Description
                            </label>
                            <input
                                type="text"
                                id="description"
                                name="description"
                                value={formData.description}
                                onChange={handleInputChange}
                                placeholder="E.g. Monthly Salary"
                                className={inputClasses}
                                required
                                disabled={submitting}
                            />
                        </div>

                        <div>
                            <label htmlFor="date" className="block text-xs font-black text-[var(--color-text-secondary)] uppercase tracking-widest mb-2 opacity-60">
                                Date
                            </label>
                            <input
                                type="date"
                                id="date"
                                name="date"
                                value={formData.date}
                                onChange={handleInputChange}
                                className={inputClasses}
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
                        {submitting ? 'Processing...' : 'Add Income Entry'}
                    </button>
                </form>
            </div>

            {/* Income List */}
            <div className="bg-[var(--color-surface)] rounded-2xl shadow-sm border border-[var(--color-border)] overflow-hidden animate-fade-in stagger-2">
                <div className="px-8 py-6 border-b border-[var(--color-border)]">
                    <h2 className="text-lg font-black text-[var(--color-text-primary)] uppercase tracking-widest opacity-80">Inflow History</h2>
                </div>

                {incomes.length === 0 ? (
                    <div className="text-center py-16">
                        <div className="inline-flex p-6 bg-[var(--color-bg-hover)] rounded-3xl mb-4">
                            <TrendingUp className="h-10 w-10 text-[var(--color-text-muted)] opacity-30" />
                        </div>
                        <h3 className="text-sm font-black text-[var(--color-text-primary)] uppercase tracking-widest mb-1">No incomes logged</h3>
                        <p className="text-xs font-bold text-[var(--color-text-secondary)] opacity-60">Start by adding your first income entry above.</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="bg-[var(--color-table-header)] border-b border-[var(--color-border)]">
                                    <th className="px-8 py-4 text-left text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Amount</th>
                                    <th className="px-8 py-4 text-left text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Source</th>
                                    <th className="px-8 py-4 text-left text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Date</th>
                                    <th className="px-8 py-4 text-right text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-[var(--color-table-border)]">
                                {incomes.map((income, index) => (
                                    <tr key={income.id} className={`hover:bg-[var(--color-table-hover)] transition-colors animate-fade-in stagger-${index % 5 + 1}`}>
                                        <td className="px-8 py-5 whitespace-nowrap text-sm font-black text-emerald-600">
                                            {formatCurrency(income.amount)}
                                        </td>
                                        <td className="px-8 py-5 whitespace-nowrap text-sm font-bold text-[var(--color-text-primary)]">
                                            {income.source}
                                        </td>
                                        <td className="px-8 py-5 whitespace-nowrap text-xs font-bold text-[var(--color-text-secondary)] opacity-70">
                                            {new Date(income.date).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
                                        </td>
                                        <td className="px-8 py-5 whitespace-nowrap text-right">
                                            <button
                                                onClick={() => handleDelete(income.id)}
                                                className="p-2 text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/30 rounded-lg transition-all active:scale-90"
                                                title="Delete entry"
                                            >
                                                <LogOut className="h-4 w-4 rotate-180" />
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );

};
export default IncomePage;