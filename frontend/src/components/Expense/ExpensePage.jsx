import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const ExpensePage = () => {
    const [expenses, setExpenses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({
        amount: '',
        description: '',
        category: '',
        date: new Date().toISOString().split('T')[0]
    });

    useEffect(() => {
        fetchExpenses();
    }, []);

    const fetchExpenses = async () => {
        try {
            const data = await api.getExpenses();
            setExpenses(data);
        } catch (error) {
            console.error('Error fetching expenses:', error);
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
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.createExpense({
                ...formData,
                amount: parseFloat(formData.amount)
            });
            setFormData({
                amount: '',
                description: '',
                category: '',
                date: new Date().toISOString().split('T')[0]
            });
            fetchExpenses(); // Refresh the list
        } catch (error) {
            console.error('Error creating expense:', error);
        }
    };

    const handleDelete = async (id) => {
        try {
            await api.deleteExpense(id);
            fetchExpenses(); // Refresh the list
        } catch (error) {
            console.error('Error deleting expense:', error);
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1 className="text-2xl font-bold mb-4">Expense Management</h1>

            {/* Add Expense Form */}
            <form onSubmit={handleSubmit} className="mb-6 p-4 bg-white rounded shadow">
                <h2 className="text-lg font-semibold mb-2">Add New Expense</h2>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <input
                        type="number"
                        name="amount"
                        value={formData.amount}
                        onChange={handleInputChange}
                        placeholder="Amount"
                        className="p-2 border rounded"
                        required
                    />
                    <input
                        type="text"
                        name="description"
                        value={formData.description}
                        onChange={handleInputChange}
                        placeholder="Description"
                        className="p-2 border rounded"
                        required
                    />
                    <input
                        type="text"
                        name="category"
                        value={formData.category}
                        onChange={handleInputChange}
                        placeholder="Category"
                        className="p-2 border rounded"
                        required
                    />
                    <input
                        type="date"
                        name="date"
                        value={formData.date}
                        onChange={handleInputChange}
                        className="p-2 border rounded"
                        required
                    />
                </div>
                <button type="submit" className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                    Add Expense
                </button>
            </form>

            {/* Expense List */}
            <div className="bg-white rounded shadow">
                <h2 className="text-lg font-semibold p-4">Your Expenses</h2>
                <table className="w-full">
                    <thead>
                        <tr className="border-b">
                            <th className="text-left p-4">Amount</th>
                            <th className="text-left p-4">Description</th>
                            <th className="text-left p-4">Category</th>
                            <th className="text-left p-4">Date</th>
                            <th className="text-left p-4">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {expenses.map(expense => (
                            <tr key={expense.id} className="border-b">
                                <td className="p-4">${expense.amount}</td>
                                <td className="p-4">{expense.description}</td>
                                <td className="p-4">{expense.category}</td>
                                <td className="p-4">{new Date(expense.date).toLocaleDateString()}</td>
                                <td className="p-4">
                                    <button
                                        onClick={() => handleDelete(expense.id)}
                                        className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ExpensePage;