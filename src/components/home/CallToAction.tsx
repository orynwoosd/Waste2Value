import { Link } from "react-router-dom";

export default function CallToAction() {
  return (
    <section className="pb-16">
      <div className="max-w-7xl mx-auto px-6">
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-green-800 to-green-700 px-8 py-10 lg:px-12 lg:py-12">
          {/* Background decoration */}
          <div className="absolute -bottom-10 -right-10 w-56 h-56 rounded-full bg-green-600 opacity-20"></div>
          <div className="absolute top-0 left-1/2 w-40 h-40 rounded-full bg-green-500 opacity-10"></div>

          <div className="relative flex flex-col lg:flex-row items-center justify-between gap-8">
            <div className="text-white">
              <h2 className="text-3xl font-bold">
                Ready to make a difference?
              </h2>

              <p className="mt-3 text-green-100 max-w-xl">
                Join thousands of households in Yaoundé VI that are helping
                create a cleaner environment through responsible waste
                segregation and recycling.
              </p>
            </div>

            <Link
              to="/register"
              className="bg-white text-green-700 font-semibold px-8 py-4 rounded-xl hover:bg-gray-100 transition"
            >
              Register Today
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
