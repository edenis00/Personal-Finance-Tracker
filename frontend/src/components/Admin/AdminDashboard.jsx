import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const AdminDashboard = () => {
    const [dashboard, setDashboard] = useState(null);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchDashboard();
        fetchUsers();
    }, []);

    const fetchDashboard = async () => {
        try {
            const data = await api.getAdminDashboard();
            setDashboard(data);
        } catch (error) {
            console.error('Error fetching dashboard:', error);
        }
    };

    const fetchUsers = async () => {
        try {
            const data = await api.getAllUsers();
            setUsers(data);
        } catch (error) {
            console.error('Error fetching users:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleActivateDeactivate = async (userId, activate) => {
        try {
            await api.activateDeactivateUser(userId, activate);
            fetchUsers(); // Refresh the list
        } catch (error) {
            console.error('Error updating user status:', error);
        }
    };

    const handleDeleteUser = async (userId) => {
        if (window.confirm('Are you sure you want to delete this user?')) {
            try {
                await api.deleteUserById(userId);
                fetchUsers(); // Refresh the list
            } catch (error) {
                console.error('Error deleting user:', error);
            }
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>

            {/* Dashboard Stats */}
            {dashboard && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white p-4 rounded shadow">
                        <h3 className="text-lg font-semibold">Total Users</h3>
                        <p className="text-2xl">{dashboard.total_users}</p>
                    </div>
                    <div className="bg-white p-4 rounded shadow">
                        <h3 className="text-lg font-semibold">Total Income</h3>
                        <p className="text-2xl">${dashboard.total_income}</p>
                    </div>
                    <div className="bg-white p-4 rounded shadow">
                        <h3 className="text-lg font-semibold">Total Expenses</h3>
                        <p className="text-2xl">${dashboard.total_expenses}</p>
                    </div>
                    <div className="bg-white p-4 rounded shadow">
                        <h3 className="text-lg font-semibold">Total Savings</h3>
                        <p className="text-2xl">${dashboard.total_savings}</p>
                    </div>
                </div>
            )}

            {/* Users Management */}
            <div className="bg-white rounded shadow">
                <h2 className="text-lg font-semibold p-4">User Management</h2>
                <table className="w-full">
                    <thead>
                        <tr className="border-b">
                            <th className="text-left p-4">Email</th>
                            <th className="text-left p-4">Name</th>
                            <th className="text-left p-4">Role</th>
                            <th className="text-left p-4">Balance</th>
                            <th className="text-left p-4">Status</th>
                            <th className="text-left p-4">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(user => (
                            <tr key={user.id} className="border-b">
                                <td className="p-4">{user.email}</td>
                                <td className="p-4">{user.first_name} {user.last_name}</td>
                                <td className="p-4">{user.role}</td>
                                <td className="p-4">${user.balance}</td>
                                <td className="p-4">{user.is_active ? 'Active' : 'Inactive'}</td>
                                <td className="p-4">
                                    <button
                                        onClick={() => handleActivateDeactivate(user.id, !user.is_active)}
                                        className={`px-2 py-1 rounded mr-2 ${user.is_active ? 'bg-yellow-500' : 'bg-green-500'} text-white`}
                                    >
                                        {user.is_active ? 'Deactivate' : 'Activate'}
                                    </button>
                                    <button
                                        onClick={() => handleDeleteUser(user.id)}
                                        className="px-2 py-1 bg-red-500 text-white rounded"
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

export default AdminDashboard;