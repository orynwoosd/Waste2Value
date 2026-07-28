import logo from "../../assets/images/logo.png";
import bins from "../../assets/images/bins.png";

export default function AccountSidebar() {
  return (
    <div className="bg-gradient-to-b from-lime-50 to-white p-10 flex flex-col">
      <img src={logo} alt="Waste2Value" className="w-44" />

      <div className="mt-20">
        <h2 className="text-4xl font-bold">
          Create Your
          <br />
          Account
        </h2>

        <p className="mt-5 text-gray-600 leading-7">
          Join us in building a cleaner and greener Yaoundé VI.
        </p>
      </div>

      <div className="mt-auto">
        <img src={bins} alt="" className="w-48 mx-auto" />

        <div className="mt-10 space-y-5">
          <div className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-full bg-green-700 text-white flex items-center justify-center">
              1
            </div>

            <span className="font-medium">Account Info</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-full bg-gray-300">2</div>

            <span className="text-gray-500">Location Info</span>
          </div>
        </div>
      </div>
    </div>
  );
}
