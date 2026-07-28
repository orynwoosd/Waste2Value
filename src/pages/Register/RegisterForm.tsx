interface Props {
  step: number;
  setStep: (step: number) => void;
}

export default function RegisterForm({ step, setStep }: Props) {
  return (
    <div className="p-12">
      <div>
        <p className="text-green-700 font-semibold">Step {step} of 2</p>

        <h2 className="text-4xl font-bold mt-2">
          {step === 1 ? "Account Information" : "Location Information"}
        </h2>

        <p className="text-gray-500 mt-3">
          Let's start with your basic information.
        </p>
      </div>

      {step === 1 && (
        <div className="mt-10">
          <div className="grid md:grid-cols-2 gap-6">
            <input placeholder="First Name" className="border rounded-lg p-4" />

            <input placeholder="Last Name" className="border rounded-lg p-4" />

            <input
              placeholder="Phone Number"
              className="border rounded-lg p-4"
            />

            <input placeholder="Email" className="border rounded-lg p-4" />

            <input
              type="password"
              placeholder="Password"
              className="border rounded-lg p-4"
            />

            <input
              type="password"
              placeholder="Confirm Password"
              className="border rounded-lg p-4"
            />
          </div>

          <button
            onClick={() => setStep(2)}
            className="mt-10 w-full bg-green-700 text-white py-4 rounded-xl hover:bg-green-800"
          >
            Next Step →
          </button>
        </div>
      )}

      {step === 2 && (
        <div className="mt-10">
          <div className="space-y-6">
            <input
              placeholder="Quarter"
              className="border rounded-lg p-4 w-full"
            />

            <input
              placeholder="Street Address"
              className="border rounded-lg p-4 w-full"
            />

            <input
              placeholder="Nearest Landmark"
              className="border rounded-lg p-4 w-full"
            />

            <input type="file" className="border rounded-lg p-4 w-full" />
          </div>

          <div className="flex gap-5 mt-10">
            <button
              onClick={() => setStep(1)}
              className="flex-1 border rounded-xl py-4"
            >
              Back
            </button>

            <button className="flex-1 bg-green-700 text-white rounded-xl">
              Create Account
            </button>
          </div>
        </div>
      )}

      <div className="mt-8 text-center">
        Already have an account?
        <span className="text-green-700 font-semibold cursor-pointer">
          Login
        </span>
      </div>
    </div>
  );
}
