
import React from 'react';

const Loader = ({ fullScreen = false }) => {
    const loaderContent = (
        <div className="flex flex-col items-center justify-center gap-4">
            <div className="relative w-16 h-16">
                {/* Outer Ring */}
                <div className="absolute inset-0 rounded-full border-4 border-[var(--color-border)] opacity-30"></div>
                {/* Spinning Ring */}
                <div className="absolute inset-0 rounded-full border-4 border-t-blue-500 border-r-transparent border-b-transparent border-l-transparent animate-spin"></div>
                {/* Inner Glow */}
                <div className="absolute inset-2 rounded-full border-2 border-blue-400/20 blur-[2px]"></div>
            </div>
            <div className="flex flex-col items-center">
                <span className="text-lg font-medium text-[var(--color-text-primary)] animate-pulse">
                    Personal Finance Tracker
                </span>
                <span className="text-sm text-[var(--color-text-secondary)]">
                    Optimizing your financial data...
                </span>
            </div>
        </div>
    );

    if (fullScreen) {
        return (
            <div className="fixed inset-0 z-[100] flex items-center justify-center bg-[var(--color-bg-primary)]">
                {loaderContent}
            </div>
        );
    }

    return (
        <div className="flex items-center justify-center p-8">
            {loaderContent}
        </div>
    );
};

export default Loader;
