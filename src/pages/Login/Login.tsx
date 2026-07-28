import LoginSidebar from "./LoginSidebar";
import LoginForm from "./LoginForm";

export default function Login() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-8">
      <div className="w-full max-w-7xl bg-white rounded-3xl shadow-xl overflow-hidden">
        <div className="grid lg:grid-cols-12">
          <div className="lg:col-span-4">
            <LoginSidebar />
          </div>

          <div className="lg:col-span-6">
            <LoginForm />
          </div>
        </div>
      </div>
    </div>
  );
}
