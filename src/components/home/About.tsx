import { CheckCircle2, ArrowRight, ShieldCheck, Leaf } from "lucide-react";
import aboutImage from "../../assets/images/about us.jpeg";

const features = [
  "Easy household waste pickup",
  "Verified waste collectors",
  "Sustainable recycling practices",
  "Marketplace for recycled products",
];

export default function About() {
  return (
    <section id="about" className="relative overflow-hidden bg-white py-24">
      <div className="mx-auto flex max-w-7xl flex-col items-center gap-16 px-6 lg:flex-row">
        {/* Left Side: Styled Image Stack */}
        <div className="relative flex-1 w-full">
          {/* Main Image Container */}
          <div className="relative overflow-hidden rounded-3xl border border-gray-100 shadow-2xl shadow-green-950/10 bg-gray-100">
            <img
              src={aboutImage}
              alt="About Waste2Value"
              className="h-[460px] w-full object-cover transition-transform duration-700 hover:scale-105"
            />
            {/* Subtle Gradient Vignette */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />
          </div>

          {/* Floating Eco Badge Overlay (Top Left) */}
          <div className="absolute -top-5 -left-5 hidden sm:flex items-center gap-2 rounded-2xl bg-white p-4 shadow-xl border border-gray-100">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-100 text-green-600">
              <Leaf size={20} />
            </div>
            <div>
              <p className="text-xs font-bold text-gray-900">100% Eco-Driven</p>
              <p className="text-[10px] text-gray-500">Circular Economy</p>
            </div>
          </div>

          {/* Floating Impact Card Overlay (Bottom Right) */}
          <div className="absolute -bottom-6 -right-6 hidden sm:flex items-center gap-4 rounded-2xl bg-gradient-to-br from-green-800 to-green-700 p-5 text-white shadow-2xl shadow-green-900/30">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/10 backdrop-blur-md">
              <ShieldCheck size={24} className="text-green-300" />
            </div>
            <div>
              <p className="text-2xl font-extrabold leading-tight">100+</p>
              <p className="text-xs text-green-100 font-light">
                Tons Waste Recycled
              </p>
            </div>
          </div>
        </div>

        {/* Right Side: Content & Features */}
        <div className="flex-1">
          {/* Pill Badge */}
          <span className="inline-flex items-center gap-1.5 rounded-full bg-green-100 px-3.5 py-1 text-xs font-semibold uppercase tracking-wider text-green-800">
            About Us
          </span>

          <h2 className="mt-4 text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl lg:text-5xl leading-tight">
            Turning Domestic Waste Into{" "}
            <span className="text-green-600">Real Opportunity</span>
          </h2>

          <p className="mt-10 text-base text-gray-600 sm:text-lg font-light leading-relaxed">
            Waste2Value is a digital domestic waste recovery platform built to
            connect households, collectors, and recycling companies seamlessly.
            Our mission is to transform everyday refuse into valuable circular
            products while keeping our communities clean.
          </p>

          {/* Features Grid */}
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
            {features.map((feature) => (
              <div
                key={feature}
                className="flex items-center gap-3 rounded-xl border border-gray-100 bg-gray-50/60 p-3.5 transition-all hover:bg-white hover:border-green-200 hover:shadow-sm"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-green-100 text-green-600 shrink-0">
                  <CheckCircle2 size={18} />
                </div>
                <span className="text-sm font-medium text-gray-800">
                  {feature}
                </span>
              </div>
            ))}
          </div>

          {/* Action Button */}
          <div className="mt-10">
            <button className="group inline-flex items-center gap-2 rounded-xl bg-green-600 px-7 py-3.5 text-sm font-semibold text-white shadow-lg shadow-green-600/20 transition-all duration-300 hover:bg-green-700 hover:shadow-xl hover:shadow-green-600/30 active:scale-95">
              Learn More About Our Mission
              <ArrowRight
                size={16}
                className="transition-transform group-hover:translate-x-1"
              />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
