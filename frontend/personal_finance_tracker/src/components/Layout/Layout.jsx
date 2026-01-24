import React from 'react';
import { Outlet } from 'react-router-dom';

const Layout = ({ user, onLogout }) => {
    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <div className="w-64 bg-white shadow-md">
                <div className="p-4">
                    <h2 className="text-xl font-bold">Personal Finance Tracker</h2>
                </div>
                <nav className="mt-4">
                    <a href="/dashboard" className="block px-4 py-2 text-gray-700 hover:bg-gray-200">Dashboard</a>
                    <a href="/income" className="block px-4 py-2 text-gray-700 hover:bg-gray-200">Income</a>
                    <a href="/expenses" className="block px-4 py-2 text-gray-700 hover:bg-gray-200">Expenses</a>
                    <a href="/savings" className="block px-4 py-2 text-gray-700 hover:bg-gray-200">Savings</a>
                    <a href="/profile" className="block px-4 py-2 text-gray-700 hover:bg-gray-200">Profile</a>
                    {user?.role === 'admin' && (
                        <a href="/admin" className="block px-4 py-2 text-gray-700 hover:bg-gray-200">Admin</a>
                    )}
                    <button onClick={onLogout} className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-200">Logout</button>
                </nav>
            </div>
            {/* Main content */}
            <div className="flex-1 p-4">
                <Outlet />
            </div>
        </div>
    );
};

export default Layout;