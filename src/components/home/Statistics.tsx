import { Users, Recycle, Building2, Star, TrendingUp } from "lucide-react";

const stats = [
  {
    value: "3k+",
    label: "Households Registered",
    description: "Actively sorting & recycling",
    icon: Users,
    trend: "+18% this month",
  },
  {
    value: "85%",
    label: "Waste Diverted",
    description: "Saved from local landfills",
    icon: Recycle,
    trend: "High efficiency",
  },
  {
    value: "120+",
    label: "Recycling Partners",
    description: "Verified green processors",
    icon: Building2,
    trend: "Growing network",
  },
  {
    value: "4.9/5",
    label: "User Satisfaction",
    description: "Based on 1,200+ reviews",
    icon: Star,
    trend: "Top rated",
  },
];

export default function Statistics() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-gray-50 via-green-50/40 to-white py-20">
      {/* Subtle Background Pattern Mesh */}
      <div className="absolute inset-0 bg-[radial-gradient(#22c55e_1px,transparent_1px)] [background-size:24px_24px] opacity-[0.07]" />

      <div className="relative mx-auto max-w-7xl px-6">
        {/* Optional Section Subheader for context */}
        <div className="mx-auto mb-14 max-w-2xl text-center">
          <span className="rounded-full bg-green-100 px-3.5 py-1 text-xs font-semibold uppercase tracking-wider text-green-800">
            Our Environmental Impact
          </span>
          <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Making a measurable difference
          </h2>
        </div>

        {/* Stats Grid */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => {
            const Icon = stat.icon;
            return (
              <div
                key={stat.label}
                className="group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-gray-100 bg-white p-7 shadow-sm transition-all duration-300 hover:-translate-y-1.5 hover:border-green-200 hover:shadow-xl hover:shadow-green-900/5"
              >
                {/* Top Green Accent Line on Hover */}
                <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-green-500 to-emerald-400 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />

                <div>
                  {/* Top Bar with Icon & Trend */}
                  <div className="flex items-center justify-between">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-green-50 text-green-600 transition-colors duration-300 group-hover:bg-green-600 group-hover:text-white">
                      <Icon size={24} />
                    </div>

                    <span className="flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
                      <TrendingUp size={12} />
                      {stat.trend}
                    </span>
                  </div>

                  {/* Main Metric Value */}
                  <div className="mt-6 text-4xl font-extrabold tracking-tight text-gray-900 group-hover:text-green-600 transition-colors">
                    {stat.value}
                  </div>

                  {/* Label */}
                  <h3 className="mt-1 text-base font-semibold text-gray-800">
                    {stat.label}
                  </h3>
                </div>

                {/* Subtitle / Description */}
                <p className="mt-3 border-t border-gray-50 pt-3 text-xs text-gray-500">
                  {stat.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
