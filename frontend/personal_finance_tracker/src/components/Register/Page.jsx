import { Wallet, Eye, EyeOff } from "lucide-react"
import { useState } from "react"
import { Link } from "react-router-dom"

export default function RegisterPage() {

    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        confirmPassword: ""
    })

    const [showPassword, setShowPassword] = useState(false)
    const [showConfirmPassword, setShowConfirmPassword] = useState(false)

    const handleChange = (e) => {
        const { id, value } = e.target
        setFormData(prev => ({
            ...prev,
            [id]: value
        }))
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        // Handle registration logic here
        if (formData.password !== formData.confirmPassword) {
            alert("Passwords do not match")
            return
        }

        // redirect here after successful registration
    }
    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
            <div className="w-full max-w-lg">
                <div className="text-center mb-8">
                    <div className="inline-flex items-center h-16 w-16 justify-center rounded-2xl bg-blue-600 text-white mb-4">
                        <Wallet className="h-8 w-8" />
                    </div>
                    <h2 className="text-3xl font-bold text-black mb-2">Create Account</h2>
                    <p className="text-gray-500">Start tracking your finances today</p>
                </div>
                <div className="bg-white rounded-2xl p-8 shadow-lg">
                    <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label htmlFor="firstName" className="text-sm font-medium">First Name</label>
                            <input
                                id="firstName"
                                type="text"
                                placeholder="First Name"
                                required
                                value={formData.firstName}
                                onChange={handleChange}
                                className="w-full h-11 rounded-lg border border-gray-300 px-4 mt-1"
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="lastName" className="text-sm font-medium">Last Name</label>
                            <input
                                id="lastName"
                                type="text"
                                placeholder="Last Name"
                                value={formData.lastName}
                                onChange={handleChange}
                                className="w-full h-11 rounded-lg border border-gray-300 px-4 mt-1"
                            />
                        </div>
                        <div className="col-span-2">
                            <label htmlFor="email" className="text-sm font-medium">Email Address</label>
                            <input
                                id="email"
                                type="email"
                                placeholder="example@gmail.com"
                                value={formData.email}
                                onChange={handleChange}
                                className="w-full h-11 rounded-lg border border-gray-300 px-4 mt-1"
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="password" className="text-sm font-medium">Password</label>
                            <div className="relative">
                                <input
                                    id="password"
                                    type={showPassword ? "text" : "password"}
                                    placeholder="Password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    className="w-full h-11 rounded-lg border border-gray-300 px-4 mt-1"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 transition-colors"
                                >
                                    {showPassword ? (<EyeOff className="h-5 w-5" />) : <Eye className="h-5 w-5" />}
                                </button>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label htmlFor="confirmPassword" className="text-sm font-medium">Confirm Password</label>
                            <div className="relative">
                                <input
                                    id="confirmPassword"
                                    type={showConfirmPassword ? "text" : "password"}
                                    placeholder="Confirm Password"
                                    value={formData.confirmPassword}
                                    onChange={handleChange}
                                    className="w-full h-11 rounded-lg border border-gray-300 px-4 mt-1"
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 transition-colors"
                                >
                                    {showConfirmPassword ? (<EyeOff className="h-5 w-5" />) : <Eye className="h-5 w-5" />}
                                </button>
                            </div>
                        </div>
                        <div className="col-span-2 flex items-center space-x-2">
                            <input type="checkbox" name="terms" id="terms" />
                            <p className='text-center text-xs text-gray-600'>
                                {" "}By continuing, you agree to our Terms of Service and Privacy Policy
                            </p>
                        </div>
                        <button type="submit" className="col-span-2 bg-blue-700 text-white py-3 rounded-lg mt-2 hover:bg-blue-800 cursor-pointer">Create Account</button>
                    </form>

                    <div className="text-center mt-6">
                        <p className="text-gray-600 text-sm">
                            Already have an account {" "}
                            <Link to="/login" className="text-blue-700 font-medium hover:underline">Sign In</Link>
                        </p>
                    </div>

                </div>
            </div>
        </div>
    )
}