import { useState } from "react";
import RegisterSidebar from "./RegisterSidebar";
import RegisterForm from "./RegisterForm";

export default function Register() {
  const [step, setStep] = useState(1);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-8">
      <div className="w-full max-w-7xl bg-white rounded-3xl shadow-xl overflow-hidden">
        <div className="grid lg:grid-cols-12">
          <div className="lg:col-span-4">
            <RegisterSidebar step={step} />
          </div>

          <div className="lg:col-span-8">
            <RegisterForm step={step} setStep={setStep} />
          </div>
        </div>
      </div>
    </div>
  );
}
