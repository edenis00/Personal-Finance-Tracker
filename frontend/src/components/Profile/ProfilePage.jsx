import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const ProfilePage = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({ email: '', first_name: '', last_name: '' });
    const [formErrors, setFormErrors] = useState({});

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

    const inputCls = (hasError) => `w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] outline-none transition-colors ${hasError ? 'border-red-300 dark:border-red-700' : 'border-[var(--color-input-border)]'}`;

    if (loading) return (<div className="flex items-center justify-center min-h-64"><div className="text-lg text-[var(--color-text-secondary)]">Loading profile...</div></div>);

    if (error && !profile) return (
        <div className="max-w-2xl mx-auto p-6">
            <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-md mb-4">{error}</div>
            <button onClick={fetchProfile} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Try Again</button>
        </div>
    );

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">Profile Settings</h1>
                <button onClick={fetchProfile} className="px-4 py-2 bg-[var(--color-bg-hover)] text-[var(--color-text-secondary)] rounded-md hover:bg-[var(--color-border)] transition-colors">Refresh</button>
            </div>
            {error && (<div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-md">{error}</div>)}
            {success && (<div className="bg-green-50 dark:bg-green-950/50 border border-green-200 dark:border-green-800 text-green-700 dark:text-green-400 px-4 py-3 rounded-md">{success}</div>)}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Profile Overview */}
                <div className="lg:col-span-1">
                    <div className="bg-[var(--color-surface)] rounded-lg shadow-sm border border-[var(--color-border)] p-6">
                        <div className="text-center">
                            <div className="mx-auto h-24 w-24 rounded-full bg-blue-600 flex items-center justify-center mb-4">
                                <span className="text-2xl font-bold text-white">{profile.first_name?.[0]}{profile.last_name?.[0]}</span>
                            </div>
                            <h2 className="text-xl font-semibold text-[var(--color-text-primary)]">{profile.first_name} {profile.last_name}</h2>
                            <p className="text-[var(--color-text-secondary)]">{profile.email}</p>
                            <div className="mt-4">
                                <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${profile.role === 'admin' ? 'bg-purple-100 dark:bg-purple-900/50 text-purple-800 dark:text-purple-300' : 'bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300'}`}>
                                    {profile.role?.charAt(0).toUpperCase() + profile.role?.slice(1)}
                                </span>
                            </div>
                        </div>
                        <div className="mt-6 pt-6 border-t border-[var(--color-border)]">
                            <div className="flex justify-between items-center">
                                <span className="text-sm font-medium text-[var(--color-text-muted)]">Account Balance</span>
                                <span className="text-lg font-semibold text-green-600 dark:text-green-400">${parseFloat(profile.balance || 0).toFixed(2)}</span>
                            </div>
                        </div>
                        <div className="mt-4 pt-4 border-t border-[var(--color-border)]">
                            <div className="text-sm text-[var(--color-text-muted)]">Member since: {new Date(profile.created_at).toLocaleDateString()}</div>
                        </div>
                    </div>
                </div>

                {/* Profile Details/Edit Form */}
                <div className="lg:col-span-2">
                    <div className="bg-[var(--color-surface)] rounded-lg shadow-sm border border-[var(--color-border)] p-6">
                        {!editing ? (
                            <>
                                <div className="flex items-center justify-between mb-6">
                                    <h2 className="text-xl font-semibold text-[var(--color-text-primary)]">Profile Information</h2>
                                    <button onClick={() => setEditing(true)} className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">Edit Profile</button>
                                </div>
                                <div className="space-y-4">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">First Name</label>
                                            <div className="p-3 bg-[var(--color-bg-muted)] rounded-md text-[var(--color-text-primary)]">{profile.first_name || 'Not set'}</div>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">Last Name</label>
                                            <div className="p-3 bg-[var(--color-bg-muted)] rounded-md text-[var(--color-text-primary)]">{profile.last_name || 'Not set'}</div>
                                        </div>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">Email Address</label>
                                        <div className="p-3 bg-[var(--color-bg-muted)] rounded-md text-[var(--color-text-primary)]">{profile.email}</div>
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">Account Role</label>
                                            <div className="p-3 bg-[var(--color-bg-muted)] rounded-md text-[var(--color-text-primary)] capitalize">{profile.role || 'User'}</div>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">Account Status</label>
                                            <div className="p-3 bg-[var(--color-bg-muted)] rounded-md">
                                                <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${profile.is_active ? 'bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-300' : 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300'}`}>
                                                    {profile.is_active ? 'Active' : 'Inactive'}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </>
                        ) : (
                            <>
                                <div className="flex items-center justify-between mb-6">
                                    <h2 className="text-xl font-semibold text-[var(--color-text-primary)]">Edit Profile</h2>
                                </div>
                                <form onSubmit={handleSubmit} className="space-y-4">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label htmlFor="first_name" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">First Name *</label>
                                            <input type="text" id="first_name" name="first_name" value={formData.first_name} onChange={handleInputChange} className={inputCls(formErrors.first_name)} disabled={saving} />
                                            {formErrors.first_name && <p className="mt-1 text-sm text-red-600 dark:text-red-400">{formErrors.first_name}</p>}
                                        </div>
                                        <div>
                                            <label htmlFor="last_name" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">Last Name *</label>
                                            <input type="text" id="last_name" name="last_name" value={formData.last_name} onChange={handleInputChange} className={inputCls(formErrors.last_name)} disabled={saving} />
                                            {formErrors.last_name && <p className="mt-1 text-sm text-red-600 dark:text-red-400">{formErrors.last_name}</p>}
                                        </div>
                                    </div>
                                    <div>
                                        <label htmlFor="email" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-1">Email Address *</label>
                                        <input type="email" id="email" name="email" value={formData.email} onChange={handleInputChange} className={inputCls(formErrors.email)} disabled={saving} />
                                        {formErrors.email && <p className="mt-1 text-sm text-red-600 dark:text-red-400">{formErrors.email}</p>}
                                    </div>
                                    <div className="flex space-x-3 pt-4">
                                        <button type="submit" disabled={saving} className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">{saving ? 'Saving...' : 'Save Changes'}</button>
                                        <button type="button" onClick={handleCancel} disabled={saving} className="px-6 py-3 bg-[var(--color-bg-hover)] text-[var(--color-text-secondary)] rounded-md hover:bg-[var(--color-border)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors">Cancel</button>
                                    </div>
                                </form>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ProfilePage;