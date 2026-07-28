import logo from "../../assets/images/logo.jpeg";
import LoginImage from "../../assets/images/login illustration.png";

export default function LoginSidebar() {
  return (
    <div className="bg-gradient-to-b from-green-900 to-green-700 text-white h-full p-10 flex flex-col">
      <img src={logo} alt="Waste2Value" className="w-40" />

      <div className="mt-16">
        <h1 className="text-4xl font-bold">Welcome Back!</h1>

        <p className="mt-4 text-green-100 leading-7">
          Login to your account and continue making a difference.
        </p>
      </div>

      <div className="flex-1 flex items-end">
        <img src={LoginImage} alt="Login Illustration" className="w-full" />
      </div>
    </div>
  );
}
