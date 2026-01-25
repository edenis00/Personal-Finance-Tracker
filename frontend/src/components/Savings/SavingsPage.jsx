import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const SavingsPage = () => {
    const [savings, setSavings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({
        goal: '',
        amount: ''
    });

    useEffect(() => {
        fetchSavings();
    }, []);

    const fetchSavings = async () => {
        try {
            const data = await api.getSavings();
            setSavings(data);
        } catch (error) {
            console.error('Error fetching savings:', error);
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
            await api.createSaving({
                ...formData,
                amount: parseFloat(formData.amount)
            });
            setFormData({
                goal: '',
                amount: ''
            });
            fetchSavings(); // Refresh the list
        } catch (error) {
            console.error('Error creating saving:', error);
        }
    };

    const handleDelete = async (id) => {
        try {
            await api.deleteSaving(id);
            fetchSavings(); // Refresh the list
        } catch (error) {
            console.error('Error deleting saving:', error);
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1 className="text-2xl font-bold mb-4">Savings Management</h1>

            {/* Add Savings Form */}
            <form onSubmit={handleSubmit} className="mb-6 p-4 bg-white rounded shadow">
                <h2 className="text-lg font-semibold mb-2">Add New Savings Goal</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        type="text"
                        name="goal"
                        value={formData.goal}
                        onChange={handleInputChange}
                        placeholder="Savings Goal"
                        className="p-2 border rounded"
                        required
                    />
                    <input
                        type="number"
                        name="amount"
                        value={formData.amount}
                        onChange={handleInputChange}
                        placeholder="Target Amount"
                        className="p-2 border rounded"
                        required
                    />
                </div>
                <button type="submit" className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                    Add Savings Goal
                </button>
            </form>

            {/* Savings List */}
            <div className="bg-white rounded shadow">
                <h2 className="text-lg font-semibold p-4">Your Savings Goals</h2>
                <table className="w-full">
                    <thead>
                        <tr className="border-b">
                            <th className="text-left p-4">Goal</th>
                            <th className="text-left p-4">Target Amount</th>
                            <th className="text-left p-4">Current Amount</th>
                            <th className="text-left p-4">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {savings.map(saving => (
                            <tr key={saving.id} className="border-b">
                                <td className="p-4">{saving.goal}</td>
                                <td className="p-4">${saving.amount}</td>
                                <td className="p-4">${saving.current_amount || 0}</td>
                                <td className="p-4">
                                    <button
                                        onClick={() => handleDelete(saving.id)}
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

export default SavingsPage;