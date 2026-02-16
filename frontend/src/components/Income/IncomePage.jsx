import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const IncomePage = () => {
    const [incomes, setIncomes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
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

    const inputClasses = "w-full p-3 border border-[var(--color-input-border)] rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] outline-none transition-colors";

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-64">
                <div className="text-lg text-[var(--color-text-secondary)]">Loading incomes...</div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">Income Management</h1>
                <button
                    onClick={fetchIncomes}
                    className="px-4 py-2 bg-[var(--color-bg-hover)] text-[var(--color-text-secondary)] rounded-md hover:bg-[var(--color-border)] transition-colors"
                >
                    Refresh
                </button>
            </div>

            {error && (
                <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-md">
                    {error}
                </div>
            )}

            {/* Add Income Form */}
            <div className="bg-[var(--color-surface)] rounded-lg shadow-sm border border-[var(--color-border)] p-6">
                <h2 className="text-xl font-semibold mb-4 text-[var(--color-text-primary)]">Add New Income</h2>

                <form onSubmit={handleSubmit} className="space-y-4">
                    {formError && (
                        <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-3 py-2 rounded-md text-sm">
                            {formError}
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label htmlFor="amount" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">
                                Amount ($)
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
                            <label htmlFor="description" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">
                                Description
                            </label>
                            <input
                                type="text"
                                id="description"
                                name="description"
                                value={formData.description}
                                onChange={handleInputChange}
                                placeholder="Salary, Freelance, etc."
                                className={inputClasses}
                                required
                                disabled={submitting}
                            />
                        </div>

                        <div>
                            <label htmlFor="date" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">
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
                        className="w-full md:w-auto px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        {submitting ? 'Adding Income...' : 'Add Income'}
                    </button>
                </form>
            </div>

            {/* Income List */}
            <div className="bg-[var(--color-surface)] rounded-lg shadow-sm border border-[var(--color-border)] overflow-hidden">
                <div className="px-6 py-4 border-b border-[var(--color-border)]">
                    <h2 className="text-xl font-semibold text-[var(--color-text-primary)]">Your Incomes</h2>
                    <p className="text-sm text-[var(--color-text-secondary)] mt-1">Track and manage your income sources</p>
                </div>

                {incomes.length === 0 ? (
                    <div className="text-center py-12">
                        <div className="text-[var(--color-text-muted)] text-4xl mb-4">💰</div>
                        <h3 className="text-lg font-medium text-[var(--color-text-primary)] mb-2">No incomes yet</h3>
                        <p className="text-[var(--color-text-secondary)]">Add your first income source above to get started.</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-[var(--color-table-header)]">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
                                        Amount
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
                                        Description
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
                                        Date
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-[var(--color-table-border)]">
                                {incomes.map(income => (
                                    <tr key={income.id} className="hover:bg-[var(--color-table-hover)] transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-[var(--color-text-primary)]">
                                            ${parseFloat(income.amount).toFixed(2)}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-[var(--color-text-primary)]">
                                            {income.source}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-[var(--color-text-secondary)]">
                                            {new Date(income.date).toLocaleDateString()}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                            <button
                                                onClick={() => handleDelete(income.id)}
                                                className="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300 px-3 py-1 rounded-md hover:bg-red-50 dark:hover:bg-red-950/50 transition-colors"
                                            >
                                                Delete
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

}
export default IncomePage;