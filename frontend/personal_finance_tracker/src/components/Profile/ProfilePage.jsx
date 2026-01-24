import React, { useState, useEffect } from 'react';
import api from '../../services/api';

const ProfilePage = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({
        email: '',
        first_name: '',
        last_name: ''
    });

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const data = await api.getUserProfile();
            setProfile(data);
            setFormData({
                email: data.email || '',
                first_name: data.first_name || '',
                last_name: data.last_name || ''
            });
        } catch (error) {
            console.error('Error fetching profile:', error);
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
            await api.updateUserProfile(formData);
            setEditing(false);
            fetchProfile(); // Refresh the profile
        } catch (error) {
            console.error('Error updating profile:', error);
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1 className="text-2xl font-bold mb-4">User Profile</h1>

            {!editing ? (
                <div className="bg-white p-6 rounded shadow">
                    <h2 className="text-lg font-semibold mb-4">Profile Information</h2>
                    <p><strong>Email:</strong> {profile.email}</p>
                    <p><strong>First Name:</strong> {profile.first_name}</p>
                    <p><strong>Last Name:</strong> {profile.last_name}</p>
                    <p><strong>Role:</strong> {profile.role}</p>
                    <p><strong>Balance:</strong> ${profile.balance}</p>
                    <button
                        onClick={() => setEditing(true)}
                        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                        Edit Profile
                    </button>
                </div>
            ) : (
                <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow">
                    <h2 className="text-lg font-semibold mb-4">Edit Profile</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            placeholder="Email"
                            className="p-2 border rounded"
                            required
                        />
                        <input
                            type="text"
                            name="first_name"
                            value={formData.first_name}
                            onChange={handleInputChange}
                            placeholder="First Name"
                            className="p-2 border rounded"
                        />
                        <input
                            type="text"
                            name="last_name"
                            value={formData.last_name}
                            onChange={handleInputChange}
                            placeholder="Last Name"
                            className="p-2 border rounded"
                        />
                    </div>
                    <div className="mt-4">
                        <button type="submit" className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 mr-2">
                            Save Changes
                        </button>
                        <button
                            type="button"
                            onClick={() => setEditing(false)}
                            className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            )}
        </div>
    );
};

export default ProfilePage;