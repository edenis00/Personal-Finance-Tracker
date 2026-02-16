import { Wallet, Eye, EyeOff, Sun, Moon } from "lucide-react"
import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import api from '../../services/api'
import { useTheme } from '../../context/ThemeContext'

export default function RegisterPage() {
    const navigate = useNavigate()
    const { theme, toggleTheme } = useTheme()

    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        confirmPassword: ""
    })

    const [showPassword, setShowPassword] = useState(false)
    const [showConfirmPassword, setShowConfirmPassword] = useState(false)
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const handleChange = (e) => {
        const { id, value } = e.target
        setFormData(prev => ({
            ...prev,
            [id]: value
        }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')

        if (formData.password !== formData.confirmPassword) {
            setError("Passwords do not match")
            return
        }

        setLoading(true)
        try {
            const userData = {
                email: formData.email,
                password: formData.password,
                first_name: formData.firstName,
                last_name: formData.lastName,
            }
            await api.signup(userData)
            navigate("/login")
        } catch (error) {
            setError(error.message)
        } finally {
            setLoading(false)
        }
    }

    const inputClasses = "w-full h-11 rounded-lg border border-[var(--color-input-border)] px-4 mt-1 bg-[var(--color-input-bg)] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"

    return (
        <div className="min-h-screen bg-[var(--color-bg-primary)] flex items-center justify-center p-4 relative">
            {/* Theme Toggle */}
            <button
                onClick={toggleTheme}
                className="absolute top-4 right-4 p-3 rounded-2xl bg-[var(--color-surface)] border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:text-blue-500 hover:border-blue-500 transition-all shadow-sm"
                aria-label="Toggle theme"
            >
                {theme === 'dark' ? (
                    <Sun className="h-5 w-5 text-amber-400" />
                ) : (
                    <Moon className="h-5 w-5 text-indigo-500" />
                )}
            </button>

            <div className="w-full max-w-lg">
                <div className="text-center mb-8">
                    <div className="inline-flex items-center h-16 w-16 justify-center rounded-2xl bg-blue-600 text-white mb-4">
                        <Wallet className="h-8 w-8" />
                    </div>
                    <h2 className="text-3xl font-bold text-[var(--color-text-primary)] mb-2">Create Account</h2>
                    <p className="text-[var(--color-text-secondary)]">Start tracking your finances today</p>
                </div>
                <div className="bg-[var(--color-surface)] rounded-2xl p-8 shadow-lg border border-[var(--color-border)]">
                    <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
                        {error && (
                            <div className="col-span-2 bg-red-50 dark:bg-red-950/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-md text-sm mb-4">
                                {error}
                            </div>
                        )}
                        <div className="space-y-2">
                            <label htmlFor="firstName" className="text-sm font-medium text-[var(--color-text-primary)]">First Name</label>
                            <input
                                id="firstName"
                                type="text"
                                placeholder="First Name"
                                required
                                value={formData.firstName}
                                onChange={handleChange}
                                className={inputClasses}
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="lastName" className="text-sm font-medium text-[var(--color-text-primary)]">Last Name</label>
                            <input
                                id="lastName"
                                type="text"
                                placeholder="Last Name"
                                required
                                value={formData.lastName}
                                onChange={handleChange}
                                className={inputClasses}
                            />
                        </div>
                        <div className="col-span-2">
                            <label htmlFor="email" className="text-sm font-medium text-[var(--color-text-primary)]">Email Address</label>
                            <input
                                id="email"
                                type="email"
                                placeholder="example@gmail.com"
                                required
                                value={formData.email}
                                onChange={handleChange}
                                className={inputClasses}
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="password" className="text-sm font-medium text-[var(--color-text-primary)]">Password</label>
                            <div className="relative">
                                <input
                                    id="password"
                                    type={showPassword ? "text" : "password"}
                                    placeholder="Password"
                                    required
                                    value={formData.password}
                                    onChange={handleChange}
                                    className={inputClasses}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] transition-colors"
                                >
                                    {showPassword ? (<EyeOff className="h-5 w-5" />) : <Eye className="h-5 w-5" />}
                                </button>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label htmlFor="confirmPassword" className="text-sm font-medium text-[var(--color-text-primary)]">Confirm Password</label>
                            <div className="relative">
                                <input
                                    id="confirmPassword"
                                    type={showConfirmPassword ? "text" : "password"}
                                    placeholder="Confirm Password"
                                    required
                                    value={formData.confirmPassword}
                                    onChange={handleChange}
                                    className={inputClasses}
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] transition-colors"
                                >
                                    {showConfirmPassword ? (<EyeOff className="h-5 w-5" />) : <Eye className="h-5 w-5" />}
                                </button>
                            </div>
                        </div>
                        <div className="col-span-2 flex items-center space-x-2">
                            <input type="checkbox" name="terms" id="terms" required className="accent-blue-600" />
                            <p className='text-center text-xs text-[var(--color-text-secondary)]'>
                                By continuing, you agree to our Terms of Service and Privacy Policy
                            </p>
                        </div>
                        <button
                            type="submit"
                            disabled={loading}
                            className="col-span-2 bg-blue-700 text-white py-3 rounded-lg mt-2 hover:bg-blue-800 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            {loading ? 'Creating Account...' : 'Create Account'}
                        </button>
                    </form>

                    <div className="text-center mt-6">
                        <p className="text-[var(--color-text-secondary)] text-sm">
                            Already have an account {" "}
                            <Link to="/login" className="text-blue-600 dark:text-blue-400 font-medium hover:underline">Sign In</Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}