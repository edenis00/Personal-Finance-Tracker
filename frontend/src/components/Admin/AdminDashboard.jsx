import React, { useState, useEffect } from 'react';
import { Users, Shield, RefreshCw, Trash2, CheckCircle, XCircle, Wallet } from 'lucide-react';
import { useCurrency } from '../../context/CurrencyContext';
import api from '../../services/api';
import Loader from '../UI/Loader';

const AdminDashboard = () => {
    const [dashboard, setDashboard] = useState(null);
    const [users, setUsers] = useState([]);
    const [refreshing, setRefreshing] = useState(false);
    const { formatCurrency } = useCurrency();
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
        <div className="space-y-8 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-black text-[var(--color-text-primary)] tracking-tight">System Administration</h1>
                    <p className="text-sm font-bold text-[var(--color-text-secondary)] mt-1 uppercase tracking-widest opacity-60">Global overview and user management</p>
                </div>
                <button
                    onClick={() => { setLoading(true); fetchDashboard(); fetchUsers(); }}
                    className="px-8 py-4 bg-indigo-600 text-white text-xs font-black uppercase tracking-widest rounded-xl hover:bg-indigo-700 transition-all active:scale-95"
                >
                    Refresh Records
                </button>
            </div>

            {error && (
                <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 rounded-2xl p-6 flex items-center animate-fade-in">
                    <AlertCircle className="h-5 w-5 text-red-500 mr-4" />
                    <span className="text-sm font-bold text-red-700 dark:text-red-400">{error}</span>
                </div>
            )}

            {dashboard && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-[var(--color-surface)] p-8 rounded-2xl shadow-sm border border-[var(--color-border)] animate-fade-in stagger-1">
                        <div className="flex items-center">
                            <div className="p-3 bg-indigo-100 dark:bg-indigo-900/50 rounded-xl">
                                <Users className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
                            </div>
                            <div className="ml-5">
                                <p className="text-xs font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Total Users</p>
                                <p className="text-2xl font-black text-[var(--color-text-primary)] mt-1">{dashboard.total_users}</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-[var(--color-surface)] p-8 rounded-2xl shadow-sm border border-[var(--color-border)] animate-fade-in stagger-2">
                        <div className="flex items-center">
                            <div className="p-3 bg-emerald-100 dark:bg-emerald-900/50 rounded-xl">
                                <TrendingUp className="h-6 w-6 text-emerald-600 dark:text-emerald-400" />
                            </div>
                            <div className="ml-5">
                                <p className="text-xs font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Total Income</p>
                                <p className="text-2xl font-black text-emerald-600 mt-1">{formatCurrency(dashboard.total_income || 0)}</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-[var(--color-surface)] p-8 rounded-2xl shadow-sm border border-[var(--color-border)] animate-fade-in stagger-3">
                        <div className="flex items-center">
                            <div className="p-3 bg-rose-100 dark:bg-rose-900/50 rounded-xl">
                                <TrendingDown className="h-6 w-6 text-rose-600 dark:text-rose-400" />
                            </div>
                            <div className="ml-5">
                                <p className="text-xs font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Total Expenses</p>
                                <p className="text-2xl font-black text-rose-600 mt-1">{formatCurrency(dashboard.total_expenses || 0)}</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-[var(--color-surface)] p-8 rounded-2xl shadow-sm border border-[var(--color-border)] animate-fade-in stagger-4">
                        <div className="flex items-center">
                            <div className="p-3 bg-amber-100 dark:bg-amber-900/50 rounded-xl">
                                <PiggyBank className="h-6 w-6 text-amber-600 dark:text-amber-400" />
                            </div>
                            <div className="ml-5">
                                <p className="text-xs font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Total Savings</p>
                                <p className="text-2xl font-black text-amber-600 mt-1">{formatCurrency(dashboard.total_savings || 0)}</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            <div className="bg-[var(--color-surface)] rounded-2xl shadow-sm border border-[var(--color-border)] overflow-hidden animate-fade-in stagger-5">
                <div className="px-8 py-6 border-b border-[var(--color-border)]">
                    <h2 className="text-lg font-black text-[var(--color-text-primary)] uppercase tracking-widest opacity-80">Directory of Users</h2>
                    <p className="text-xs font-bold text-[var(--color-text-secondary)] mt-1 opacity-60">Administrative control over all accounts</p>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="bg-[var(--color-table-header)] border-b border-[var(--color-border)]">
                                <th className="text-left px-8 py-4 text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Contact</th>
                                <th className="text-left px-8 py-4 text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Identify</th>
                                <th className="text-left px-8 py-4 text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Access</th>
                                <th className="text-left px-8 py-4 text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Capital</th>
                                <th className="text-left px-8 py-4 text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Status</th>
                                <th className="text-right px-8 py-4 text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em]">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-[var(--color-table-border)]">
                            {users.length === 0 ? (
                                <tr>
                                    <td colSpan="6" className="px-8 py-16 text-center text-xs font-bold text-[var(--color-text-muted)] opacity-60">No user records detected in the vault</td>
                                </tr>
                            ) : (
                                users.map((user, index) => (
                                    <tr key={user.id} className={`hover:bg-[var(--color-table-hover)] transition-colors animate-fade-in stagger-${(index % 5) + 1}`}>
                                        <td className="px-8 py-5 whitespace-nowrap text-sm font-bold text-[var(--color-text-primary)]">{user.email}</td>
                                        <td className="px-8 py-5 whitespace-nowrap text-sm font-bold text-[var(--color-text-secondary)]">{user.first_name} {user.last_name}</td>
                                        <td className="px-8 py-5 whitespace-nowrap">
                                            <span className={`inline-flex px-3 py-1 text-[10px] font-black uppercase tracking-widest rounded-lg ${user.role === 'admin' ? 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300' : 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300'}`}>
                                                {user.role}
                                            </span>
                                        </td>
                                        <td className="px-8 py-5 whitespace-nowrap text-sm font-black text-emerald-600">{formatCurrency(user.balance || 0)}</td>
                                        <td className="px-8 py-5 whitespace-nowrap">
                                            <div className="flex items-center gap-2">
                                                <div className={`h-1.5 w-1.5 rounded-full ${user.is_active ? 'bg-emerald-500' : 'bg-rose-500'}`} />
                                                <span className={`text-[10px] font-black uppercase tracking-widest ${user.is_active ? 'text-emerald-600' : 'text-rose-600'}`}>
                                                    {user.is_active ? 'Active' : 'Locked'}
                                                </span>
                                            </div>
                                        </td>
                                        <td className="px-8 py-5 whitespace-nowrap text-right space-x-3">
                                            <button
                                                onClick={() => handleActivateDeactivate(user.id, !user.is_active)}
                                                disabled={actionLoading === user.id}
                                                className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all active:scale-95 ${user.is_active ? 'bg-amber-100 dark:bg-amber-900/50 text-amber-700 dark:text-amber-300 hover:bg-amber-200' : 'bg-emerald-100 dark:bg-emerald-900/50 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-200'} disabled:opacity-50`}
                                            >
                                                {actionLoading === user.id && <Loader2 className="h-3 w-3 animate-spin inline mr-2" />}
                                                {user.is_active ? 'Deactivate' : 'Activate'}
                                            </button>
                                            <button
                                                onClick={() => handleDeleteUser(user.id)}
                                                disabled={actionLoading === user.id}
                                                className="px-4 py-2 bg-rose-100 dark:bg-rose-900/50 text-rose-700 dark:text-rose-300 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-rose-200 transition-all active:scale-95 disabled:opacity-50"
                                            >
                                                {actionLoading === user.id && <Loader2 className="h-3 w-3 animate-spin inline mr-2" />}
                                                Delete user
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