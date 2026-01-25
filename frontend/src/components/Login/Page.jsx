import { Wallet, Eye, EyeOff } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../../services/api'



export default function LoginPage({ onLogin }) {


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
        <div className="min-h-screen bg-gray-100 flex justify-center items-start p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-8">
                    <div className='inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-700 text-white mb-4'>
                        <Wallet className='h-8 w-8' />
                    </div>
                    <h2 className="text-3xl font-bold text-black mb-2">Welcome back</h2>
                    <p className="text-gray-600">Sign in to your Finance Tracker account</p>
                </div>

                <div className="bg-white rounded-2xl p-8 shadow-lg">
                    <form onSubmit={handleSubmit} className='space-y-6'>
                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md text-sm">
                                {error}
                            </div>
                        )}
                        <div className='space-y-2'>
                            <label htmlFor="email" className='text-sm font-medium'>
                                Email Address
                            </label>
                            <input
                                id="email"
                                type="email"
                                placeholder="example@example.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="w-full h-11 rounded-md border-gray-300 border px-4"
                            />
                        </div>

                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="text-sm font-medium">Password</label>
                                <Link to="#" className="text-gray-600 text-blue-700 hover:underline">Forgot password?</Link>
                            </div>
                            <div className="relative">
                                <input
                                    id='password'
                                    type={showPassword ? "text" : "password"}
                                    placeholder='password'
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                    className='w-full h-11 rounded-md border border-gray-300 px-2'
                                />
                                <button
                                    type='button'
                                    onClick={() => setShowPassword(!showPassword)}
                                    className='absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 transition-colors'
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
                        <p className="text-sm text-gray-600">
                            Don't have an account?{' '}
                            <Link to="/register" className="text-blue-700 font-medium hover:underline">Sign Up</Link>
                        </p>
                    </div>
                </div>
                <p className='text-center text-xs text-gray-600 mt-8'>
                    By continuing, you agree to our Terms of Service and Privacy Policy
                </p>
            </div>
        </div>
    )
}