import React, { useState, useEffect } from 'react';
import { AlertCircle, Users, TrendingUp, TrendingDown, PiggyBank, Loader2 } from 'lucide-react';
import api from '../../services/api';
import Loader from '../UI/Loader';

const AdminDashboard = () => {
    const [dashboard, setDashboard] = useState(null);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [actionLoading, setActionLoading] = useState(null);

    useEffect(() => { fetchDashboard(); fetchUsers(); }, []);

    const fetchDashboard = async () => {
        try { const response = await api.getAdminDashboard(); setDashboard(response.data); setError(null); }
        catch (error) { setError('Failed to load dashboard data.'); }
    };

    const fetchUsers = async () => {
        try { const response = await api.getAllUsers(); setUsers(response.data); setError(null); }
        catch (error) { setError('Failed to load users data.'); }
        finally { setLoading(false); }
    };

    const handleActivateDeactivate = async (userId, activate) => {
        setActionLoading(userId);
        try { await api.activateDeactivateUser(userId, activate); await fetchUsers(); setError(null); }
        catch (error) { setError(`Failed to ${activate ? 'activate' : 'deactivate'} user.`); }
        finally { setActionLoading(null); }
    };

    const handleDeleteUser = async (userId) => {
        if (window.confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
            setActionLoading(userId);
            try { await api.deleteUserById(userId); await fetchUsers(); setError(null); }
            catch (error) { setError('Failed to delete user.'); }
            finally { setActionLoading(null); }
        }
    };

    if (loading) return <Loader />;

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">Admin Dashboard</h1>
                <button onClick={() => { setLoading(true); fetchDashboard(); fetchUsers(); }} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">Refresh Data</button>
            </div>
            {error && (
                <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-center">
                    <AlertCircle className="h-5 w-5 text-red-500 mr-3" />
                    <span className="text-red-700 dark:text-red-400">{error}</span>
                </div>
            )}
            {dashboard && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-[var(--color-surface)] p-6 rounded-xl shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center">
                            <div className="p-2 bg-blue-100 dark:bg-blue-900/50 rounded-lg"><Users className="h-6 w-6 text-blue-600 dark:text-blue-400" /></div>
                            <div className="ml-4"><p className="text-sm font-medium text-[var(--color-text-secondary)]">Total Users</p><p className="text-2xl font-bold text-[var(--color-text-primary)]">{dashboard.total_users}</p></div>
                        </div>
                    </div>
                    <div className="bg-[var(--color-surface)] p-6 rounded-xl shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center">
                            <div className="p-2 bg-green-100 dark:bg-green-900/50 rounded-lg"><TrendingUp className="h-6 w-6 text-green-600 dark:text-green-400" /></div>
                            <div className="ml-4"><p className="text-sm font-medium text-[var(--color-text-secondary)]">Total Income</p><p className="text-2xl font-bold text-[var(--color-text-primary)]">${dashboard.total_income?.toLocaleString() || '0'}</p></div>
                        </div>
                    </div>
                    <div className="bg-[var(--color-surface)] p-6 rounded-xl shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center">
                            <div className="p-2 bg-red-100 dark:bg-red-900/50 rounded-lg"><TrendingDown className="h-6 w-6 text-red-600 dark:text-red-400" /></div>
                            <div className="ml-4"><p className="text-sm font-medium text-[var(--color-text-secondary)]">Total Expenses</p><p className="text-2xl font-bold text-[var(--color-text-primary)]">${dashboard.total_expenses?.toLocaleString() || '0'}</p></div>
                        </div>
                    </div>
                    <div className="bg-[var(--color-surface)] p-6 rounded-xl shadow-sm border border-[var(--color-border)]">
                        <div className="flex items-center">
                            <div className="p-2 bg-purple-100 dark:bg-purple-900/50 rounded-lg"><PiggyBank className="h-6 w-6 text-purple-600 dark:text-purple-400" /></div>
                            <div className="ml-4"><p className="text-sm font-medium text-[var(--color-text-secondary)]">Total Savings</p><p className="text-2xl font-bold text-[var(--color-text-primary)]">${dashboard.total_savings?.toLocaleString() || '0'}</p></div>
                        </div>
                    </div>
                </div>
            )}
            <div className="bg-[var(--color-surface)] rounded-xl shadow-sm border border-[var(--color-border)] overflow-hidden">
                <div className="px-6 py-4 border-b border-[var(--color-border)]">
                    <h2 className="text-xl font-semibold text-[var(--color-text-primary)]">User Management</h2>
                    <p className="text-sm text-[var(--color-text-secondary)] mt-1">Manage user accounts and permissions</p>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-[var(--color-table-header)]">
                            <tr>
                                <th className="text-left px-6 py-3 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Email</th>
                                <th className="text-left px-6 py-3 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Name</th>
                                <th className="text-left px-6 py-3 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Role</th>
                                <th className="text-left px-6 py-3 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Balance</th>
                                <th className="text-left px-6 py-3 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Status</th>
                                <th className="text-left px-6 py-3 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-[var(--color-table-border)]">
                            {users.length === 0 ? (
                                <tr><td colSpan="6" className="px-6 py-8 text-center text-[var(--color-text-muted)]">No users found</td></tr>
                            ) : (
                                users.map(user => (
                                    <tr key={user.id} className="hover:bg-[var(--color-table-hover)] transition-colors">
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-[var(--color-text-primary)]">{user.email}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-[var(--color-text-primary)]">{user.first_name} {user.last_name}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${user.role === 'admin' ? 'bg-purple-100 dark:bg-purple-900/50 text-purple-800 dark:text-purple-300' : 'bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300'}`}>{user.role}</span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-[var(--color-text-primary)]">${user.balance?.toLocaleString() || '0'}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${user.is_active ? 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300' : 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300'}`}>{user.is_active ? 'Active' : 'Inactive'}</span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                                            <button onClick={() => handleActivateDeactivate(user.id, !user.is_active)} disabled={actionLoading === user.id}
                                                className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${user.is_active ? 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-300 hover:bg-yellow-200 dark:hover:bg-yellow-900/80' : 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300 hover:bg-green-200 dark:hover:bg-green-900/80'} disabled:opacity-50 disabled:cursor-not-allowed`}>
                                                {actionLoading === user.id ? (<Loader2 className="h-4 w-4 animate-spin inline mr-1" />) : null}
                                                {user.is_active ? 'Deactivate' : 'Activate'}
                                            </button>
                                            <button onClick={() => handleDeleteUser(user.id)} disabled={actionLoading === user.id}
                                                className="px-3 py-1 bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300 rounded-md text-sm font-medium hover:bg-red-200 dark:hover:bg-red-900/80 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                                                {actionLoading === user.id ? (<Loader2 className="h-4 w-4 animate-spin inline mr-1" />) : null}
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;