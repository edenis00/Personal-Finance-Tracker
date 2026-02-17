import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import Loader from '../UI/Loader';
import { RefreshCw, Globe } from 'lucide-react';
import { useCurrency } from '../../context/CurrencyContext';

const ProfilePage = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({ email: '', first_name: '', last_name: '' });
    const [formErrors, setFormErrors] = useState({});
    const { currency, setCurrency, formatCurrency, currencyOptions } = useCurrency();

    useEffect(() => { fetchProfile(); }, []);

    const fetchProfile = async () => {
        try {
            setError('');
            const response = await api.getUserProfile();
            const userData = response.data;
            setProfile(userData);
            setFormData({ email: userData.email || '', first_name: userData.first_name || '', last_name: userData.last_name || '' });
        } catch (error) { setError('Failed to load profile.'); } finally { setLoading(false); }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        if (formErrors[name]) setFormErrors(prev => ({ ...prev, [name]: '' }));
    };

    const validateForm = () => {
        const errors = {};
        if (!formData.email.trim()) errors.email = 'Email is required';
        else if (!/\S+@\S+\.\S+/.test(formData.email)) errors.email = 'Please enter a valid email';
        if (!formData.first_name.trim()) errors.first_name = 'First name is required';
        if (!formData.last_name.trim()) errors.last_name = 'Last name is required';
        setFormErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); setSuccess('');
        if (!validateForm()) return;
        setSaving(true);
        try {
            await api.updateUserProfile(formData);
            setSuccess('Profile updated successfully!');
            setEditing(false);
            fetchProfile();
        } catch (error) { setError(error.message || 'Failed to update profile.'); } finally { setSaving(false); }
    };

    const handleCancel = () => {
        setFormData({ email: profile.email || '', first_name: profile.first_name || '', last_name: profile.last_name || '' });
        setFormErrors({});
        setEditing(false);
    };

    // Removed local formatCurrency as it's now provided by CurrencyContext

    const inputCls = (hasError) => `w-full p-4 border rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] outline-none transition-all ${hasError ? 'border-red-300 dark:border-red-700' : 'border-[var(--color-input-border)]'}`;

    if (loading) return <Loader />;

    if (error && !profile) return (
        <div className="max-w-2xl mx-auto p-12 text-center animate-fade-in">
            <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-sm font-bold text-red-700 dark:text-red-400 px-6 py-4 rounded-2xl mb-6">{error}</div>
            <button onClick={fetchProfile} className="px-8 py-4 bg-indigo-600 text-white text-xs font-black uppercase tracking-widest rounded-xl hover:bg-indigo-700 transition-all active:scale-95">Try Again</button>
        </div>
    );

    return (
        <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-black text-[var(--color-text-primary)] tracking-tight">Profile Settings</h1>
                    <p className="text-sm font-bold text-[var(--color-text-secondary)] mt-1 uppercase tracking-widest opacity-60">Manage your account and preferences</p>
                </div>
                <button
                    onClick={fetchProfile}
                    className="p-3 bg-[var(--color-bg-hover)] text-[var(--color-text-secondary)] rounded-xl hover:bg-[var(--color-border)] transition-all active:scale-95"
                >
                    <RefreshCw className="h-5 w-5" />
                </button>
            </div>

            {error && (
                <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-sm font-bold text-red-700 dark:text-red-400 px-4 py-3 rounded-xl animate-fade-in">
                    {error}
                </div>
            )}

            {success && (
                <div className="bg-green-50 dark:bg-green-950/50 border border-green-200 dark:border-green-800 text-sm font-bold text-green-700 dark:text-green-400 px-4 py-3 rounded-xl animate-fade-in">
                    {success}
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Profile Overview */}
                <div className="lg:col-span-1 animate-fade-in stagger-1">
                    <div className="bg-[var(--color-surface)] rounded-2xl shadow-sm border border-[var(--color-border)] p-8">
                        <div className="text-center">
                            <div className="mx-auto h-28 w-28 rounded-3xl bg-indigo-600 flex items-center justify-center mb-6 shadow-lg shadow-indigo-500/30 transform rotate-3">
                                <span className="text-3xl font-black text-white -rotate-3 uppercase">
                                    {profile.first_name?.[0]}{profile.last_name?.[0]}
                                </span>
                            </div>
                            <h2 className="text-xl font-black text-[var(--color-text-primary)] tracking-tight">
                                {profile.first_name} {profile.last_name}
                            </h2>
                            <p className="text-sm font-bold text-[var(--color-text-secondary)] mt-1 opacity-60">
                                {profile.email}
                            </p>
                            <div className="mt-4">
                                <span className={`inline-flex px-3 py-1 text-[10px] font-black uppercase tracking-widest rounded-lg ${profile.role === 'admin' ? 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300' : 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300'}`}>
                                    {profile.role || 'Member'}
                                </span>
                            </div>
                        </div>
                        <div className="mt-8 pt-8 border-t border-[var(--color-border)]">
                            <div className="flex justify-between items-center">
                                <span className="text-xs font-black text-[var(--color-text-muted)] uppercase tracking-widest opacity-60">Capital</span>
                                <span className="text-xl font-black text-emerald-600">
                                    {formatCurrency(profile.balance || 0)}
                                </span>
                            </div>
                        </div>
                        <div className="mt-6 pt-6 border-t border-[var(--color-border)]">
                            <div className="text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-[0.2em] opacity-40">
                                Joined {new Date(profile.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long' })}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Profile Details/Edit Form */}
                <div className="lg:col-span-2 animate-fade-in stagger-2">
                    <div className="bg-[var(--color-surface)] rounded-2xl shadow-sm border border-[var(--color-border)] p-8">
                        {!editing ? (
                            <div className="space-y-8">
                                <div className="flex items-center justify-between">
                                    <h2 className="text-lg font-black text-[var(--color-text-primary)] uppercase tracking-widest opacity-80">Credentials</h2>
                                    <button
                                        onClick={() => setEditing(true)}
                                        className="px-6 py-3 bg-indigo-600 text-white text-[10px] font-black uppercase tracking-widest rounded-xl hover:bg-indigo-700 transition-all active:scale-95"
                                    >
                                        Modify Details
                                    </button>
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">First Name</label>
                                        <div className="p-4 bg-[var(--color-bg-hover)] border border-[var(--color-border)] rounded-xl text-sm font-bold text-[var(--color-text-primary)]">
                                            {profile.first_name || 'Not provided'}
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Last Name</label>
                                        <div className="p-4 bg-[var(--color-bg-hover)] border border-[var(--color-border)] rounded-xl text-sm font-bold text-[var(--color-text-primary)]">
                                            {profile.last_name || 'Not provided'}
                                        </div>
                                    </div>
                                    <div className="space-y-2 md:col-span-2">
                                        <label className="text-[10px] font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Email Address</label>
                                        <div className="p-4 bg-[var(--color-bg-hover)] border border-[var(--color-border)] rounded-xl text-sm font-bold text-[var(--color-text-primary)] opacity-80">
                                            {profile.email}
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Account Role</label>
                                        <div className="p-4 bg-[var(--color-bg-hover)] border border-[var(--color-border)] rounded-xl text-sm font-bold text-[var(--color-text-primary)] capitalize">
                                            {profile.role || 'Standard Member'}
                                        </div>
                                    </div>
                                    <div className="space-y-2 text-right flex flex-col justify-end">
                                        <div className="flex items-center gap-3 justify-end">
                                            <div className={`h-2 w-2 rounded-full ${profile.is_active ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`} />
                                            <span className="text-[10px] font-black uppercase tracking-[0.2em] text-[var(--color-text-secondary)]">
                                                {profile.is_active ? 'Active Status' : 'Inactive'}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <form onSubmit={handleSubmit} className="space-y-8">
                                <h2 className="text-lg font-black text-[var(--color-text-primary)] uppercase tracking-widest opacity-80">Editing Profile</h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div className="space-y-2">
                                        <label htmlFor="first_name" className="text-[10px] font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">First Name *</label>
                                        <input type="text" id="first_name" name="first_name" value={formData.first_name} onChange={handleInputChange} className={inputCls(formErrors.first_name)} disabled={saving} />
                                        {formErrors.first_name && <p className="text-[10px] font-bold text-rose-500">{formErrors.first_name}</p>}
                                    </div>
                                    <div className="space-y-2">
                                        <label htmlFor="last_name" className="text-[10px] font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Last Name *</label>
                                        <input type="text" id="last_name" name="last_name" value={formData.last_name} onChange={handleInputChange} className={inputCls(formErrors.last_name)} disabled={saving} />
                                        {formErrors.last_name && <p className="text-[10px] font-bold text-rose-500">{formErrors.last_name}</p>}
                                    </div>
                                    <div className="space-y-2 md:col-span-2">
                                        <label htmlFor="email" className="text-[10px] font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Email Address *</label>
                                        <input type="email" id="email" name="email" value={formData.email} onChange={handleInputChange} className={inputCls(formErrors.email)} disabled={saving} />
                                        {formErrors.email && <p className="text-[10px] font-bold text-rose-500">{formErrors.email}</p>}
                                    </div>
                                </div>
                                <div className="flex gap-4">
                                    <button type="submit" disabled={saving} className="px-8 py-4 bg-indigo-600 text-white text-xs font-black uppercase tracking-widest rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-95">
                                        {saving ? 'Updating...' : 'Commit Changes'}
                                    </button>
                                    <button type="button" onClick={handleCancel} disabled={saving} className="px-8 py-4 bg-[var(--color-bg-hover)] text-[var(--color-text-secondary)] text-xs font-black uppercase tracking-widest border border-[var(--color-border)] rounded-xl hover:bg-[var(--color-border)] disabled:opacity-50 transition-all active:scale-95">
                                        Discard
                                    </button>
                                </div>
                            </form>
                        )}
                    </div>
                </div>

                {/* Currency Settings */}
                <div className="lg:col-span-2 animate-fade-in stagger-3">
                    <div className="bg-[var(--color-surface)] rounded-2xl shadow-sm border border-[var(--color-border)] p-8">
                        <div className="flex items-center gap-4 mb-8">
                            <div className="p-3 bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400 rounded-xl">
                                <Globe className="h-6 w-6" />
                            </div>
                            <div>
                                <h2 className="text-lg font-black text-[var(--color-text-primary)] uppercase tracking-widest opacity-80">Localization</h2>
                                <p className="text-xs font-bold text-[var(--color-text-secondary)] opacity-60">Set your preferred currency symbol</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <div className="space-y-2">
                                <label className="text-[10px] font-black text-[var(--color-text-secondary)] uppercase tracking-widest opacity-60">Display Currency</label>
                                <select
                                    value={currency}
                                    onChange={(e) => setCurrency(e.target.value)}
                                    className="w-full p-4 border border-[var(--color-border)] rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] font-bold outline-none transition-all appearance-none"
                                    style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 24 24\' stroke=\'currentColor\'%3E%3Cpath stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'2\' d=\'M19 9l-7 7-7-7\' /%3E%3C/svg%3E")', backgroundRepeat: 'no-repeat', backgroundPosition: 'right 1rem center', backgroundSize: '1.5em' }}
                                >
                                    {currencyOptions.map(opt => (
                                        <option key={opt.code} value={opt.code}>
                                            {opt.symbol} - {opt.name} ({opt.code})
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div className="flex items-end pb-1">
                                <div className="p-4 bg-[var(--color-bg-hover)] border border-[var(--color-border)] border-dashed rounded-xl w-full">
                                    <div className="text-[10px] font-black text-[var(--color-text-muted)] uppercase tracking-widest opacity-40 mb-1">Preview</div>
                                    <div className="text-xl font-black text-indigo-600">
                                        {formatCurrency(1234.56)}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;