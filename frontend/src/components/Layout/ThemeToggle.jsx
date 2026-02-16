import { Sun, Moon } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

const ThemeToggle = ({ className }) => {
    const { theme, toggleTheme } = useTheme();

    return (
        <button
            onClick={toggleTheme}
            className={className || "w-full flex items-center gap-4 px-5 py-3 text-xs font-black uppercase tracking-widest rounded-2xl bg-[var(--color-bg-primary)] border border-[var(--color-border)] shadow-sm hover:border-blue-500 hover:text-blue-500 transition-all active:scale-95 group"}
        >
            {theme === 'dark' ? (
                <>
                    <Sun className="h-4 w-4 text-amber-400 group-hover:rotate-45 transition-transform" />
                    <span>Light Mode</span>
                </>
            ) : (
                <>
                    <Moon className="h-4 w-4 text-indigo-500 group-hover:-rotate-12 transition-transform" />
                    <span>Dark Mode</span>
                </>
            )}
        </button>
    );
};

export default ThemeToggle;
