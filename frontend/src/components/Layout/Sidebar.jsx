import { useState } from 'react';
import { NavLink, useLocation, useNavigate } from 'react-router-dom';
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
    const navigate = useNavigate();
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
                    group flex items-center gap-3 px-4 py-3 text-xs font-black uppercase tracking-widest rounded-xl
                    transition-all duration-300 ease-out relative overflow-hidden
                    ${isActive
                        ? 'bg-indigo-600 text-white grow'
                        : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-hover)] hover:text-indigo-600 active:scale-95'
                    }
                `}
            >
                <Icon
                    className={`h-4 w-4 flex-shrink-0 transition-all duration-300
                        ${isActive
                            ? 'scale-110 text-white'
                            : 'text-[var(--color-text-muted)] group-hover:text-indigo-600 opacity-60 group-hover:opacity-100'
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
                    fixed inset-y-0 left-0 z-50 w-72 
                    bg-[var(--color-bg-secondary)] 
                    border-r border-[var(--color-border)]
                    flex flex-col
                    transform transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]
                    md:translate-x-0 md:static md:inset-0
                    ${isOpen ? 'translate-x-0 shadow-2xl shadow-black/50' : '-translate-x-full'}
                `}
            >
                {/* Header Section: Logo + Profile Integrated */}
                <div className="px-6 py-8 border-b border-[var(--color-border)] bg-[var(--color-bg-primary)]/50 backdrop-blur-sm">
                    <div className="flex items-center gap-4 mb-6">
                        <div className="flex-shrink-0 flex items-center justify-center w-10 h-10 rounded-xl bg-indigo-600 shadow-lg shadow-indigo-500/20 rotate-3 transform hover:rotate-0 transition-transform">
                            <Wallet className="h-5 w-5 text-white" />
                        </div>
                        <h2 className="text-sm font-black tracking-tighter text-[var(--color-text-primary)] leading-none uppercase">
                            Tracker<span className="text-indigo-600">.</span>io
                        </h2>
                    </div>
                </div>
                <button
                    onClick={onClose}
                    className="md:hidden p-3 rounded-2xl text-[var(--color-text-muted)] hover:bg-[var(--color-bg-hover)] transition-all"
                >
                    <X className="h-6 w-6" />
                </button>



                {/* Navigation */}
                <nav className="flex-1 px-4 py-6 space-y-8 overflow-y-auto custom-scrollbar">
                    {/* Main Navigation */}
                    <div className="space-y-1.5">
                        <SectionLabel>Main Menu</SectionLabel>
                        {mainNavigation.map((item) => (
                            <NavItem key={item.name} item={item} onClick={onClose} />
                        ))}
                    </div>

                    {/* Settings Section with Collapsible */}
                    <div className="space-y-1.5 pt-4">
                        <button
                            onClick={() => setSettingsOpen(!settingsOpen)}
                            className="w-full flex items-center justify-between px-4 py-2 text-[10px] font-black uppercase tracking-[0.2em] text-[var(--color-text-muted)] hover:text-indigo-600 transition-colors group"
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
                            className={`space-y-1 overflow-hidden transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] ${settingsOpen ? 'max-h-80 opacity-100' : 'max-h-0 opacity-0'
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
                <div className="mx-5 mb-4 px-4 py-3 rounded-2xl bg-[var(--color-bg-primary)] border border-[var(--color-border)] flex items-center gap-4 group cursor-pointer" onClick={() => navigate('/profile')}>
                    <div className="relative">
                        <div className="h-12 w-12 rounded-2xl bg-[var(--color-bg-hover)] border-2 border-[var(--color-border)] flex items-center justify-center group-hover:border-indigo-500 transition-colors">
                            <span className="text-indigo-600 font-black text-sm">
                                {user?.first_name?.[0]?.toUpperCase()}{user?.last_name?.[0]?.toUpperCase()}
                            </span>
                        </div>
                        <div className="absolute -bottom-1 -right-1 h-4 w-4 bg-green-500 border-2 border-[var(--color-bg-primary)] rounded-full shadow-sm"></div>
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-bold text-[var(--color-text-primary)] truncate group-hover:text-indigo-600 transition-colors">
                            {user?.first_name} {user?.last_name}
                        </p>
                        <p className="text-[10px] font-bold text-[var(--color-text-muted)] truncate uppercase tracking-widest opacity-60">
                            {user?.role || 'Elite Member'}
                        </p>
                    </div>
                    <button
                        onClick={(e) => { e.stopPropagation(); onLogout(); }}
                        className="p-2 text-[var(--color-text-muted)] hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 rounded-xl transition-all active:scale-90"
                        title="Logout"
                    >
                        <LogOut className="h-4 w-4" />
                    </button>
                </div>
            </aside >
        </>
    );
};

export default Sidebar;
