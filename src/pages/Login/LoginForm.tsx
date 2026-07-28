import { Link } from "react-router-dom";
import { Eye, Lock, Mail, CheckSquare } from "lucide-react";

export default function LoginForm() {
  return (
    <div className="px-14 py-12">
      <h2 className="text-4xl font-bold">Login to Your Account</h2>

      <p className="text-gray-500 mt-3">
        Enter your credentials to access your account.
      </p>

      <form className="mt-10 space-y-6">
        {/* Phone Number */}

        <div>
          <label className="text-sm font-semibold">Phone Number</label>

          <div className="mt-2 relative">
            <Mail className="absolute left-4 top-4 text-gray-400" size={18} />

            <input
              type="text"
              placeholder="Enter your phone number"
              className="w-full border rounded-lg py-3 pl-12 pr-4 focus:ring-2 focus:ring-green-600 outline-none"
            />
          </div>
        </div>

        {/* Password */}

        <div>
          <label className="text-sm font-semibold">Password</label>

          <div className="mt-2 relative">
            <Lock className="absolute left-4 top-4 text-gray-400" size={18} />

            <input
              type="password"
              placeholder="Enter your password"
              className="w-full border rounded-lg py-3 pl-12 pr-12 focus:ring-2 focus:ring-green-600 outline-none"
            />

            <Eye
              className="absolute right-4 top-4 text-gray-400 cursor-pointer"
              size={18}
            />
          </div>
        </div>

        {/* Remember */}

        <div className="flex justify-between items-center">
          <label className="flex items-center gap-2">
            <CheckSquare size={18} className="text-green-600" />
            Remember me
          </label>

          <Link to="/forgot-password" className="text-green-700 font-medium">
            Forgot Password?
          </Link>
        </div>

        {/* Button */}

        <button className="w-full bg-green-700 hover:bg-green-800 text-white py-3 rounded-lg font-semibold transition">
          Login
        </button>
      </form>

      <div className="text-center mt-8">
        Don't have an account?
        <Link to="/register" className="ml-2 text-green-700 font-semibold">
          Register
        </Link>
      </div>
    </div>
  );
}
