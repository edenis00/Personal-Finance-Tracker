import { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
    LayoutDashboard,
    TrendingUp,
    TrendingDown,
    PiggyBank,
    User,
    Shield,
    LogOut,
    X,
    Wallet,
    ChevronDown,
    Settings,
} from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import SettingsButton from './SettingsButton';

const Sidebar = ({ user, onLogout, isOpen, onClose }) => {
    const location = useLocation();
    const [settingsOpen, setSettingsOpen] = useState(false);

    const mainNavigation = [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Income', href: '/income', icon: TrendingUp },
        { name: 'Expenses', href: '/expenses', icon: TrendingDown },
        { name: 'Savings', href: '/savings', icon: PiggyBank },
    ];

    const settingsNavigation = [
        { name: 'Profile', href: '/profile', icon: User },
        ...(user?.role === 'admin' ? [{ name: 'Admin', href: '/admin', icon: Shield }] : []),
    ];

    const NavItem = ({ item, onClick }) => {
        const Icon = item.icon;
        const isActive = location.pathname === item.href;

        return (
            <NavLink
                to={item.href}
                onClick={onClick}
                className={`
                    group flex items-center gap-3 px-4 py-2.5 text-sm font-bold rounded-2xl
                    transition-all duration-300 ease-out relative overflow-hidden
                    ${isActive
                        ? 'bg-blue-600 text-white shadow-md active:scale-95'
                        : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-hover)] hover:text-blue-500 active:scale-95'
                    }
                `}
            >
                <Icon
                    className={`h-5 w-5 flex-shrink-0 transition-all duration-300
                        ${isActive
                            ? 'scale-110 text-white'
                            : 'text-[var(--color-text-muted)] group-hover:text-blue-500'
                        }
                    `}
                />
                <span className="relative z-10">{item.name}</span>
            </NavLink>
        );
    };

    const SectionLabel = ({ children }) => (
        <div className="px-4 py-2 text-[10px] font-bold uppercase tracking-widest text-[var(--color-text-muted)] opacity-50">
            {children}
        </div>
    );

    return (
        <>
            {/* Mobile backdrop */}
            {isOpen && (
                <div
                    className="fixed inset-0 z-40 bg-black/60 backdrop-blur-md lg:hidden transition-opacity duration-300"
                    onClick={onClose}
                />
            )}

            {/* Sidebar */}
            <aside
                className={`
                    fixed inset-y-0 left-0 z-50 w-64 
                    bg-[var(--color-bg-secondary)] 
                    border-r border-[var(--color-border)]
                    flex flex-col
                    transform transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]
                    md:translate-x-0 md:static md:inset-0
                    ${isOpen ? 'translate-x-0 shadow-2xl shadow-black/50' : '-translate-x-full'}
                `}
            >
                {/* Header / Logo */}
                <div className="flex items-center justify-between px-6 py-5">
                    <div className="flex items-center gap-4">
                        <div className="flex-shrink-0 flex items-center justify-center w-12 h-12 rounded-2xl bg-blue-600 shadow-md transform hover:rotate-6 transition-transform">
                            <Wallet className="h-6 w-6 text-white" />
                        </div>
                        <div className="min-w-0">
                            <h2 className="text-xs font-black tracking-tight text-[var(--color-text-primary)] leading-none truncate">
                                Personal Finance Tracker
                            </h2>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="md:hidden p-3 rounded-2xl text-[var(--color-text-muted)] hover:bg-[var(--color-bg-hover)] transition-all"
                    >
                        <X className="h-6 w-6" />
                    </button>
                </div>



                {/* Navigation */}
                <nav className="flex-1 px-5 space-y-1 mt-20">
                    {/* Main Navigation */}
                    <div className="space-y-2">
                        {mainNavigation.map((item) => (
                            <NavItem key={item.name} item={item} onClick={onClose} />
                        ))}
                    </div>

                    {/* Settings Section with Collapsible */}
                    <div className="space-y-1 pt-4 border-t border-[var(--color-border)] mt-4">
                        <button
                            onClick={() => setSettingsOpen(!settingsOpen)}
                            className="w-full flex items-center justify-between px-4 py-2 text-[10px] font-black uppercase tracking-[0.2em] text-[var(--color-text-muted)] hover:text-blue-500 transition-colors group"
                        >
                            <span className="flex items-center gap-3">
                                <Settings className="h-4 w-4 opacity-30 group-hover:opacity-100" />
                                Settings
                            </span>
                            <ChevronDown
                                className={`h-4 w-4 transition-transform duration-500 ${settingsOpen ? 'rotate-180' : ''}`}
                            />
                        </button>
                        <div
                            className={`space-y-2 overflow-hidden transition-all duration-700 ease-[cubic-bezier(0.4,0,0.2,1)] ${settingsOpen ? 'max-h-80 opacity-100 mt-2' : 'max-h-0 opacity-0'
                                }`}
                        >
                            <SettingsButton />

                            {settingsNavigation.map((item) => (
                                <NavItem key={item.name} item={item} onClick={onClose} />
                            ))}
                        </div>
                    </div>
                </nav>


                {/* User Profile Mini Card */}
                <div className="mx-5 mb-4 px-4 py-3 rounded-2xl bg-[var(--color-bg-primary)] border border-[var(--color-border)]">
                    <div className="flex items-center gap-3">
                        <div className="flex-shrink-0">
                            <div className="h-9 w-9 rounded-xl bg-blue-600 flex items-center justify-center shadow-md">
                                <span className="text-white font-black text-xs">
                                    {user?.first_name?.[0]?.toUpperCase()}{user?.last_name?.[0]?.toUpperCase()}
                                </span>
                            </div>
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-bold text-[var(--color-text-primary)] truncate tracking-tight">
                                {user?.first_name} {user?.last_name}
                            </p>
                            <p className="text-[9px] font-bold text-[var(--color-text-muted)] truncate uppercase tracking-[0.2em]">
                                {user?.role || 'Elite Member'}
                            </p>
                        </div>
                        <button
                            onClick={onLogout}
                            className="px-2 py-2 text-xs font-black rounded-lg tracking-widest text-red-500 hover:bg-red-500 hover:text-white transition-all active:scale-95 hover:shadow-lg cursor-pointer"
                        >
                            <LogOut className="h-4 w-4" />
                        </button>
                    </div>
                </div>
            </aside>
        </>
    );
};

export default Sidebar;
