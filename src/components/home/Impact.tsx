import { Home, Truck, Scale, Recycle, TrendingUp } from "lucide-react";

const stats = [
  {
    value: "500+",
    title: "Registered Households",
    description: "Sorting waste daily at home",
    icon: Home,
  },
  {
    value: "30+",
    title: "Active Collectors",
    description: "Verified community pickers",
    icon: Truck,
  },
  {
    value: "18 Tons",
    title: "Waste Collected",
    description: "Diverted away from streets",
    icon: Scale,
  },
  {
    value: "85%",
    title: "Waste Recycled",
    description: "Converted into valuable goods",
    icon: Recycle,
  },
];

export default function Impact() {
  return (
    <section id="impact" className="relative py-20 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        {/* Main Background Wrapper */}
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-green-900 via-green-800 to-emerald-950 px-8 py-14 lg:px-16 lg:py-16 shadow-2xl shadow-green-950/20 text-white">
          {/* Decorative Ambient Background Glows */}
          <div className="absolute -top-24 -right-24 h-96 w-96 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none" />
          <div className="absolute -bottom-24 -left-24 h-96 w-96 rounded-full bg-green-500/10 blur-3xl pointer-events-none" />

          {/* Section Header */}
          <div className="relative z-10 text-center max-w-2xl mx-auto mb-14">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-white/10 px-3.5 py-1 text-xs font-semibold uppercase tracking-wider text-green-300 backdrop-blur-md border border-white/10">
              <TrendingUp size={14} />
              Real Environmental Results
            </span>

            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight mt-4">
              Our Community Impact
            </h2>

            <p className="mt-3 text-green-100 text-base sm:text-lg font-light">
              Together with residents and local partners in Yaoundé, we are
              building a cleaner and sustainable circular economy.
            </p>
          </div>

          {/* Grid Cards */}
          <div className="relative z-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {stats.map((item) => {
              const Icon = item.icon;
              return (
                <div
                  key={item.title}
                  className="group relative flex flex-col justify-between overflow-hidden rounded-2xl bg-white/10 p-6 backdrop-blur-md border border-white/10 transition-all duration-300 hover:bg-white/20 hover:border-white/20 hover:-translate-y-1.5"
                >
                  {/* Top Bar: Icon */}
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/10 text-green-300 border border-white/10 transition-colors group-hover:bg-green-500 group-hover:text-white">
                      <Icon size={22} />
                    </div>
                  </div>

                  {/* Main Value & Title */}
                  <div>
                    <div className="text-4xl font-extrabold tracking-tight text-white group-hover:text-green-300 transition-colors">
                      {item.value}
                    </div>

                    <h3 className="mt-2 text-base font-semibold text-gray-100">
                      {item.title}
                    </h3>

                    <p className="mt-1 text-xs text-green-200/70 font-light">
                      {item.description}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
