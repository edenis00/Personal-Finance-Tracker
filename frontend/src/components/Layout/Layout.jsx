import React, { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Menu } from 'lucide-react';
import Sidebar from './Sidebar';

const Layout = ({ user, onLogout }) => {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const navigate = useNavigate();

    const handleLogout = () => {
        onLogout();
        navigate('/login');
    };

    return (
        <div className="flex h-screen bg-[var(--color-bg-primary)]">
            {/* Sidebar */}
            <Sidebar
                user={user}
                onLogout={handleLogout}
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
            />

            {/* Main content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Mobile header */}
                <div className="md:hidden bg-[var(--color-surface)] shadow-sm border-b border-[var(--color-border)] px-4 py-3 flex items-center justify-between">
                    <button
                        onClick={() => setSidebarOpen(true)}
                        className="p-2 rounded-md text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-hover)]"
                    >
                        <Menu className="h-6 w-6" />
                    </button>
                    <h1 className="text-lg font-semibold text-[var(--color-text-primary)]">Personal Finance Tracker</h1>
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