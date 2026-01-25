import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const ProfilePage = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({
        email: '',
        first_name: '',
        last_name: ''
    });
    const [formErrors, setFormErrors] = useState({});

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            setError('');
            const response = await api.getUserProfile();
            const userData = response.data;
            setProfile(userData);
            setFormData({
                email: userData.email || '',
                first_name: userData.first_name || '',
                last_name: userData.last_name || ''
            });
        } catch (error) {
            console.error('Error fetching profile:', error);
            setError('Failed to load profile. Please try again.');
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
        // Clear field-specific error when user starts typing
        if (formErrors[name]) {
            setFormErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const validateForm = () => {
        const errors = {};

        if (!formData.email.trim()) {
            errors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            errors.email = 'Please enter a valid email address';
        }

        if (!formData.first_name.trim()) {
            errors.first_name = 'First name is required';
        }

        if (!formData.last_name.trim()) {
            errors.last_name = 'Last name is required';
        }

        setFormErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (!validateForm()) {
            return;
        }

        setSaving(true);
        try {
            await api.updateUserProfile(formData);
            setSuccess('Profile updated successfully!');
            setEditing(false);
            fetchProfile(); // Refresh the profile
        } catch (error) {
            console.error('Error updating profile:', error);
            setError(error.message || 'Failed to update profile. Please try again.');
        } finally {
            setSaving(false);
        }
    };

    const handleCancel = () => {
        // Reset form data to original profile data
        setFormData({
            email: profile.email || '',
            first_name: profile.first_name || '',
            last_name: profile.last_name || ''
        });
        setFormErrors({});
        setEditing(false);
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-64">
                <div className="text-lg">Loading profile...</div>
            </div>
        );
    }

    if (error && !profile) {
        return (
            <div className="max-w-2xl mx-auto p-6">
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-4">
                    {error}
                </div>
                <button
                    onClick={fetchProfile}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                    Try Again
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-gray-900">Profile Settings</h1>
                <button
                    onClick={fetchProfile}
                    className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
                >
                    Refresh
                </button>
            </div>

            {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
                    {error}
                </div>
            )}

            {success && (
                <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-md">
                    {success}
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Profile Overview */}
                <div className="lg:col-span-1">
                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="text-center">
                            <div className="mx-auto h-24 w-24 rounded-full bg-blue-600 flex items-center justify-center mb-4">
                                <span className="text-2xl font-bold text-white">
                                    {profile.first_name?.[0]}{profile.last_name?.[0]}
                                </span>
                            </div>
                            <h2 className="text-xl font-semibold text-gray-900">
                                {profile.first_name} {profile.last_name}
                            </h2>
                            <p className="text-gray-600">{profile.email}</p>
                            <div className="mt-4">
                                <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${profile.role === 'admin'
                                    ? 'bg-purple-100 text-purple-800'
                                    : 'bg-blue-100 text-blue-800'
                                    }`}>
                                    {profile.role?.charAt(0).toUpperCase() + profile.role?.slice(1)}
                                </span>
                            </div>
                        </div>

                        <div className="mt-6 pt-6 border-t border-gray-200">
                            <div className="flex justify-between items-center">
                                <span className="text-sm font-medium text-gray-500">Account Balance</span>
                                <span className="text-lg font-semibold text-green-600">
                                    ${parseFloat(profile.balance || 0).toFixed(2)}
                                </span>
                            </div>
                        </div>

                        <div className="mt-4 pt-4 border-t border-gray-200">
                            <div className="text-sm text-gray-500">
                                Member since: {new Date(profile.created_at).toLocaleDateString()}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Profile Details/Edit Form */}
                <div className="lg:col-span-2">
                    <div className="bg-white rounded-lg shadow p-6">
                        {!editing ? (
                            <>
                                <div className="flex items-center justify-between mb-6">
                                    <h2 className="text-xl font-semibold text-gray-900">Profile Information</h2>
                                    <button
                                        onClick={() => setEditing(true)}
                                        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                                    >
                                        Edit Profile
                                    </button>
                                </div>

                                <div className="space-y-4">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                First Name
                                            </label>
                                            <div className="p-3 bg-gray-50 rounded-md text-gray-900">
                                                {profile.first_name || 'Not set'}
                                            </div>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Last Name
                                            </label>
                                            <div className="p-3 bg-gray-50 rounded-md text-gray-900">
                                                {profile.last_name || 'Not set'}
                                            </div>
                                        </div>
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Email Address
                                        </label>
                                        <div className="p-3 bg-gray-50 rounded-md text-gray-900">
                                            {profile.email}
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Account Role
                                            </label>
                                            <div className="p-3 bg-gray-50 rounded-md text-gray-900 capitalize">
                                                {profile.role || 'User'}
                                            </div>
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Account Status
                                            </label>
                                            <div className="p-3 bg-gray-50 rounded-md">
                                                <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${profile.is_active
                                                    ? 'bg-green-100 text-green-800'
                                                    : 'bg-red-100 text-red-800'
                                                    }`}>
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
                                    <h2 className="text-xl font-semibold text-gray-900">Edit Profile</h2>
                                </div>

                                <form onSubmit={handleSubmit} className="space-y-4">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div>
                                            <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-1">
                                                First Name *
                                            </label>
                                            <input
                                                type="text"
                                                id="first_name"
                                                name="first_name"
                                                value={formData.first_name}
                                                onChange={handleInputChange}
                                                className={`w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${formErrors.first_name ? 'border-red-300' : 'border-gray-300'
                                                    }`}
                                                disabled={saving}
                                            />
                                            {formErrors.first_name && (
                                                <p className="mt-1 text-sm text-red-600">{formErrors.first_name}</p>
                                            )}
                                        </div>

                                        <div>
                                            <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-1">
                                                Last Name *
                                            </label>
                                            <input
                                                type="text"
                                                id="last_name"
                                                name="last_name"
                                                value={formData.last_name}
                                                onChange={handleInputChange}
                                                className={`w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${formErrors.last_name ? 'border-red-300' : 'border-gray-300'
                                                    }`}
                                                disabled={saving}
                                            />
                                            {formErrors.last_name && (
                                                <p className="mt-1 text-sm text-red-600">{formErrors.last_name}</p>
                                            )}
                                        </div>
                                    </div>

                                    <div>
                                        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                                            Email Address *
                                        </label>
                                        <input
                                            type="email"
                                            id="email"
                                            name="email"
                                            value={formData.email}
                                            onChange={handleInputChange}
                                            className={`w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${formErrors.email ? 'border-red-300' : 'border-gray-300'
                                                }`}
                                            disabled={saving}
                                        />
                                        {formErrors.email && (
                                            <p className="mt-1 text-sm text-red-600">{formErrors.email}</p>
                                        )}
                                    </div>

                                    <div className="flex space-x-3 pt-4">
                                        <button
                                            type="submit"
                                            disabled={saving}
                                            className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                        >
                                            {saving ? 'Saving...' : 'Save Changes'}
                                        </button>
                                        <button
                                            type="button"
                                            onClick={handleCancel}
                                            disabled={saving}
                                            className="px-6 py-3 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                        >
                                            Cancel
                                        </button>
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