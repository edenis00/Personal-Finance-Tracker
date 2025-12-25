import { Wallet } from "lucide-react"

export default function Page(){

    const handleSubmit = (e) => {
        e.preventDefault()
        // Handle registration logic here
        // redirect here after successful registration
    }
    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-8">
                    <div className="inline-flex items-center h-16 w-16 justify-center rounded-2xl bg-blue-600 text-white mb-4">
                        <Wallet className="h-8 w-8"/>
                    </div>
                    <h2 className="text-3xl font-bold text-black mb-2">Create Account</h2>
                    <p className="text-gray-500">Start tracking your finances today</p>                
                </div>
                <div className="bg-white rounded-2xl p-8 shadow-lg">
                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div className="space-y-2">
                            <label htmlFor="firstName" className="text-sm font-medium">First Name</label>
                            <input 
                            id="firstName"
                            type="text"
                            placeholder="First Name"
                            required
                            className="w-full h-11 rounded-lg border border-gray-300 px-4 mt-1"
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="lastName">Last Name</label>
                            <input
                            id="lastName"
                            type="text"
                            placeholder="Last Name"
                            className="w-full h-11 rounded-lg border border-gray-300 px-4 mt-1"
                             />
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}