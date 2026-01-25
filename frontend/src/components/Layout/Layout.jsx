import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import {
    LayoutDashboard,
    TrendingUp,
    TrendingDown,
    PiggyBank,
    User,
    Shield,
    LogOut,
    Menu,
    X,
    Wallet
} from 'lucide-react';

const Layout = ({ user, onLogout }) => {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const navigate = useNavigate();

    const handleLogout = () => {
        if (window.confirm('Are you sure you want to logout?')) {
            onLogout();
            navigate('/login');
        }
    };

    const navigation = [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Income', href: '/income', icon: TrendingUp },
        { name: 'Expenses', href: '/expenses', icon: TrendingDown },
        { name: 'Savings', href: '/savings', icon: PiggyBank },
        { name: 'Profile', href: '/profile', icon: User },
    ];

    if (user?.role === 'admin') {
        navigation.push({ name: 'Admin', href: '/admin', icon: Shield });
    }

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Mobile sidebar backdrop */}
            {sidebarOpen && (
                <div
                    className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
                    onClick={() => setSidebarOpen(false)}
                />
            )}

            {/* Sidebar */}
            <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'
                }`}>
                <div className="flex items-center justify-between p-4 border-b">
                    <div className="flex items-center space-x-2">
                        <Wallet className="h-8 w-8 text-blue-600" />
                        <h2 className="text-xl font-bold text-gray-900">Finance Tracker</h2>
                    </div>
                    <button
                        onClick={() => setSidebarOpen(false)}
                        className="lg:hidden p-1 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
                    >
                        <X className="h-6 w-6" />
                    </button>
                </div>

                {/* User info */}
                <div className="px-4 py-3 border-b bg-gray-50">
                    <div className="flex items-center space-x-3">
                        <div className="flex-shrink-0">
                            <div className="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center">
                                <span className="text-white font-medium text-sm">
                                    {user?.first_name?.[0]}{user?.last_name?.[0]}
                                </span>
                            </div>
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900 truncate">
                                {user?.first_name} {user?.last_name}
                            </p>
                            <p className="text-xs text-gray-500 truncate">{user?.email}</p>
                        </div>
                    </div>
                </div>

                {/* Navigation */}
                <nav className="mt-4 px-2 space-y-1">
                    {navigation.map((item) => {
                        const Icon = item.icon;
                        return (
                            <NavLink
                                key={item.name}
                                to={item.href}
                                onClick={() => setSidebarOpen(false)}
                                className={({ isActive }) =>
                                    `group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-150 ${isActive
                                        ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700'
                                        : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                                    }`
                                }
                            >
                                <Icon
                                    className={`mr-3 h-5 w-5 flex-shrink-0 ${location.pathname === item.href
                                            ? 'text-blue-500'
                                            : 'text-gray-400 group-hover:text-gray-500'
                                        }`}
                                />
                                {item.name}
                            </NavLink>
                        );
                    })}
                </nav>

                {/* Logout button */}
                <div className="absolute bottom-0 left-0 right-0 p-4 border-t bg-white">
                    <button
                        onClick={handleLogout}
                        className="group flex items-center w-full px-3 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-red-50 hover:text-red-700 transition-colors duration-150"
                    >
                        <LogOut className="mr-3 h-5 w-5 text-gray-400 group-hover:text-red-500" />
                        Logout
                    </button>
                </div>
            </div>

            {/* Main content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Mobile header */}
                <div className="lg:hidden bg-white shadow-sm border-b px-4 py-3 flex items-center justify-between">
                    <button
                        onClick={() => setSidebarOpen(true)}
                        className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
                    >
                        <Menu className="h-6 w-6" />
                    </button>
                    <h1 className="text-lg font-semibold text-gray-900">Personal Finance Tracker</h1>
                    <div className="w-10" /> {/* Spacer for centering */}
                </div>

                {/* Page content */}
                <main className="flex-1 overflow-auto p-4 lg:p-6">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default Layout;