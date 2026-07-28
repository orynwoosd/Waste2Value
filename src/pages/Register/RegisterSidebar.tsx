import logo from "../../assets/images/logo.jpeg";
import SigninImage from "../../assets/images/register illustration.png";

interface Props {
  step: number;
}

export default function RegisterSidebar({ step }: Props) {
  return (
    <div className="h-full bg-gradient-to-b from-lime-50 to-white p-10 flex flex-col">
      <img src={logo} className="w-44" />

      <div className="mt-20">
        <h1 className="text-5xl font-bold leading-tight">
          Create Your
          <br />
          Account
        </h1>

        <p className="mt-6 text-gray-600 leading-7">
          Join us in building a cleaner and greener Yaoundé VI.
        </p>
      </div>

      <div className="flex-1 flex items-end justify-center">
        <img src={SigninImage} className="w-52" />
      </div>

      <div className="mt-10">
        <div className="flex items-center gap-4">
          <div
            className={`w-9 h-9 rounded-full flex items-center justify-center

${step === 1 ? "bg-green-700 text-white" : "bg-green-500 text-white"}`}
          >
            1
          </div>

          <span className="font-medium">Account Info</span>
        </div>

        <div className="ml-4 w-[2px] h-8 bg-gray-300" />

        <div className="flex items-center gap-4">
          <div
            className={`w-9 h-9 rounded-full flex items-center justify-center

${step === 2 ? "bg-green-700 text-white" : "bg-gray-300"}`}
          >
            2
          </div>

          <span className="text-gray-600">Location Info</span>
        </div>
      </div>
    </div>
  );
}
