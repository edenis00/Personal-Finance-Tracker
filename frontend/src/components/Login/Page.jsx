import { Wallet, Eye, EyeOff, Sun, Moon } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../services/api'
import { useTheme } from '../../context/ThemeContext'



export default function LoginPage({ onLogin }) {
    const { theme, toggleTheme } = useTheme()

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)


    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            const response = await api.login(email, password)
            onLogin(response.user)
        } catch (error) {
            setError(error.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-[var(--color-bg-primary)] flex justify-center items-start p-4 relative">
            {/* Theme Toggle */}
            <button
                onClick={toggleTheme}
                className="absolute top-4 right-4 p-3 rounded-2xl bg-[var(--color-surface)] border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:text-blue-500 hover:border-blue-500 transition-all"
                aria-label="Toggle theme"
            >
                {theme === 'dark' ? (
                    <Sun className="h-5 w-5 text-amber-400" />
                ) : (
                    <Moon className="h-5 w-5 text-indigo-500" />
                )}
            </button>

            <div className="w-full max-w-md mt-12">
                <div className="text-center mb-8">
                    <div className='inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-700 text-white mb-4'>
                        <Wallet className='h-8 w-8' />
                    </div>
                    <h2 className="text-3xl font-bold text-[var(--color-text-primary)] mb-2">Welcome back</h2>
                    <p className="text-[var(--color-text-secondary)]">Sign in to your Finance Tracker account</p>
                </div>

                <div className="bg-[var(--color-surface)] rounded-2xl p-8 shadow-lg border border-[var(--color-border)]">
                    <form onSubmit={handleSubmit} className='space-y-6'>
                        {error && (
                            <div className="bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-md text-sm">
                                {error}
                            </div>
                        )}
                        <div className='space-y-2'>
                            <label htmlFor="email" className='text-sm font-medium text-[var(--color-text-primary)]'>
                                Email Address
                            </label>
                            <input
                                id="email"
                                type="email"
                                placeholder="example@example.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="w-full h-11 rounded-md border-[var(--color-input-border)] border px-4 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
                            />
                        </div>

                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="text-sm font-medium text-[var(--color-text-primary)]">Password</label>
                                <Link to="#" className="text-blue-600 dark:text-blue-400 text-sm hover:underline">Forgot password?</Link>
                            </div>
                            <div className="relative">
                                <input
                                    id='password'
                                    type={showPassword ? "text" : "password"}
                                    placeholder='password'
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    className='w-full h-11 rounded-md border border-[var(--color-input-border)] px-4 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors'
                                />
                                <button
                                    type='button'
                                    onClick={() => setShowPassword(!showPassword)}
                                    className='absolute right-3 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] transition-colors'
                                >
                                    {showPassword ? (
                                        <EyeOff className='h-4 w-4' />
                                    ) : (
                                        <Eye className='h-4 w-4' />
                                    )}
                                </button>
                            </div>
                        </div>

                        <button
                            type='submit'
                            disabled={loading}
                            className="w-full h-11 bg-blue-700 rounded-md text-white font-medium hover:bg-blue-800 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Signing In...' : 'Sign In'}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <p className="text-sm text-[var(--color-text-secondary)]">
                            Don't have an account?{' '}
                            <Link to="/register" className="text-blue-600 dark:text-blue-400 font-medium hover:underline">Sign Up</Link>
                        </p>
                    </div>
                </div>
                <p className='text-center text-xs text-[var(--color-text-muted)] mt-4'>
                    By continuing, you agree to our Terms of Service and Privacy Policy
                </p>
            </div>
        </div>
    )
}