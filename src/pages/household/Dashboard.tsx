import React from "react";
import DashboardLayout from "../../components/Layouts/DashboardLayout";
import {
  Gift,
  Wallet,
  Recycle,
  ShoppingBag,
  TrendingUp,
  ArrowRight,
  Calendar,
  Truck,
  Star,
  Download,
  Filter,
  MoreVertical,
} from "lucide-react";

// ==========================================
// SMOOTH WAVE AREA CHART COMPONENT
// ==========================================
function SmoothWaveChart() {
  return (
    <div className="lg:col-span-6 rounded-2xl bg-white p-6 border border-slate-100 shadow-sm flex flex-col justify-between">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-bold text-slate-900 text-base">
            Waste Collection Overview
          </h3>
          <p className="text-xs text-slate-400">
            Monthly collected volume vs. target baseline (kg)
          </p>
        </div>
        <select className="text-xs font-medium border border-slate-200 rounded-lg px-2.5 py-1.5 bg-slate-50 text-slate-700 outline-none hover:bg-slate-100 transition cursor-pointer">
          <option>This Month</option>
          <option>Last Month</option>
          <option>This Year</option>
        </select>
      </div>

      {/* SVG Wave Chart Container */}
      <div className="relative w-full h-52 my-2">
        {/* Y-Axis Guidelines */}
        <div className="absolute inset-0 flex flex-col justify-between pointer-events-none text-[10px] text-slate-300 font-medium">
          <div className="border-b border-slate-100 w-full pb-0.5">4,000</div>
          <div className="border-b border-slate-100 w-full pb-0.5">3,000</div>
          <div className="border-b border-slate-100 w-full pb-0.5">2,000</div>
          <div className="border-b border-slate-100 w-full pb-0.5">1,000</div>
          <div className="border-b border-slate-200 w-full pb-0.5">0</div>
        </div>

        {/* Waves SVG */}
        <svg
          className="w-full h-full overflow-visible relative z-10"
          viewBox="0 0 500 150"
          preserveAspectRatio="none"
        >
          <defs>
            {/* Green Smooth Wave Gradient */}
            <linearGradient id="greenWave" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#22c55e" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#22c55e" stopOpacity="0.02" />
            </linearGradient>

            {/* Amber Smooth Wave Gradient */}
            <linearGradient id="amberWave" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.45" />
              <stop offset="100%" stopColor="#f59e0b" stopOpacity="0.05" />
            </linearGradient>
          </defs>

          {/* Upper Green Wave (Target / Maximum) */}
          <path
            d="M 0,65 
               C 30,25 60,35 90,50 
               C 120,65 150,20 180,15 
               C 210,10 240,60 270,65 
               C 300,70 330,40 360,30 
               C 390,20 420,45 450,25 
               C 480,10 495,35 500,45 
               L 500,150 L 0,150 Z"
            fill="url(#greenWave)"
          />
          <path
            d="M 0,65 
               C 30,25 60,35 90,50 
               C 120,65 150,20 180,15 
               C 210,10 240,60 270,65 
               C 300,70 330,40 360,30 
               C 390,20 420,45 450,25 
               C 480,10 495,35 500,45"
            fill="none"
            stroke="#16a34a"
            strokeWidth="2.5"
          />

          {/* Lower Amber Wave (Actual Collected) */}
          <path
            d="M 0,105 
               C 30,110 60,100 90,85 
               C 120,70 150,80 180,95 
               C 210,110 240,80 270,85 
               C 300,90 330,120 360,105 
               C 390,90 420,110 450,90 
               C 480,75 495,95 500,90 
               L 500,150 L 0,150 Z"
            fill="url(#amberWave)"
          />
          <path
            d="M 0,105 
               C 30,110 60,100 90,85 
               C 120,70 150,80 180,95 
               C 210,110 240,80 270,85 
               C 300,90 330,120 360,105 
               C 390,90 420,110 450,90 
               C 480,75 495,95 500,90"
            fill="none"
            stroke="#d97706"
            strokeWidth="2.5"
          />
        </svg>
      </div>

      {/* X-Axis Labels */}
      <div className="flex justify-between text-[10px] font-medium text-slate-400 px-1 pt-1 border-t border-slate-100">
        {[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31].map(
          (day) => (
            <span key={day}>{day}</span>
          ),
        )}
      </div>

      {/* Legend */}
      <div className="flex justify-center gap-6 mt-4 text-xs font-medium text-slate-600">
        <span className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-emerald-500 border border-emerald-600" />
          Target Goal (kg)
        </span>
        <span className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-amber-500 border border-amber-600" />
          Actual Collected (kg)
        </span>
      </div>
    </div>
  );
}

// ==========================================
// MAIN DASHBOARD COMPONENT
// ==========================================
export default function Dashboard() {
  const collectionHistory = [
    {
      id: "#WP-7821",
      date: "26 Jul 2026",
      time: "09:15 AM",
      category: "Organic Waste",
      categoryBadge: "bg-emerald-50 text-emerald-700 border-emerald-100",
      weight: "12.4 kg",
      collector: "Jean Pierre",
      avatar:
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80",
      points: "+120 pts",
      status: "Completed",
      statusBadge: "bg-emerald-100 text-emerald-800",
    },
    {
      id: "#WP-7710",
      date: "21 Jul 2026",
      time: "02:30 PM",
      category: "Plastic & Paper",
      categoryBadge: "bg-sky-50 text-sky-700 border-sky-100",
      weight: "8.1 kg",
      collector: "Marc Mbida",
      avatar:
        "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80",
      points: "+80 pts",
      status: "Completed",
      statusBadge: "bg-emerald-100 text-emerald-800",
    },
    {
      id: "#WP-7655",
      date: "15 Jul 2026",
      time: "11:00 AM",
      category: "Glass & Metal",
      categoryBadge: "bg-amber-50 text-amber-700 border-amber-100",
      weight: "5.0 kg",
      collector: "Jean Pierre",
      avatar:
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80",
      points: "+50 pts",
      status: "Completed",
      statusBadge: "bg-emerald-100 text-emerald-800",
    },
    {
      id: "#WP-7590",
      date: "08 Jul 2026",
      time: "04:45 PM",
      category: "Organic Waste",
      categoryBadge: "bg-emerald-50 text-emerald-700 border-emerald-100",
      weight: "14.2 kg",
      collector: "Paul Atangana",
      avatar:
        "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&auto=format&fit=crop&q=80",
      points: "+140 pts",
      status: "Completed",
      statusBadge: "bg-emerald-100 text-emerald-800",
    },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6 pb-8">
        {/* 1. Top Core Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {/* Reward Points */}
          <div className="rounded-2xl bg-emerald-50/60 p-5 border border-emerald-100 flex justify-between items-start transition hover:shadow-xs">
            <div>
              <p className="text-xs font-semibold text-emerald-800">
                Reward Points
              </p>
              <h3 className="text-2xl font-bold text-slate-900 mt-2">2,350</h3>
              <p className="text-xs font-medium text-emerald-600 mt-2 flex items-center gap-1">
                <TrendingUp className="h-3.5 w-3.5" /> +150 this month
              </p>
            </div>
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-100 text-emerald-700">
              <Gift className="h-6 w-6" />
            </div>
          </div>

          {/* Wallet Balance */}
          <div className="rounded-2xl bg-amber-50/60 p-5 border border-amber-100 flex justify-between items-start transition hover:shadow-xs">
            <div>
              <p className="text-xs font-semibold text-amber-800">
                Wallet Balance
              </p>
              <h3 className="text-2xl font-bold text-slate-900 mt-2">
                12,500 <span className="text-sm font-medium">XAF</span>
              </h3>
              <button className="text-xs font-semibold text-slate-700 hover:text-amber-700 mt-2 flex items-center gap-1 group transition-colors">
                Top up your wallet{" "}
                <ArrowRight className="h-3 w-3 transition-transform group-hover:translate-x-0.5" />
              </button>
            </div>
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-100 text-amber-700">
              <Wallet className="h-6 w-6" />
            </div>
          </div>

          {/* Collectibles */}
          <div className="rounded-2xl bg-blue-50/60 p-5 border border-blue-100 flex justify-between items-start transition hover:shadow-xs">
            <div>
              <p className="text-xs font-semibold text-blue-800">
                Collectibles
              </p>
              <h3 className="text-2xl font-bold text-slate-900 mt-2">
                15.6 kg
              </h3>
              <p className="text-xs font-medium text-blue-600 mt-2 flex items-center gap-1">
                <TrendingUp className="h-3.5 w-3.5" /> This month
              </p>
            </div>
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-100 text-blue-600">
              <Recycle className="h-6 w-6" />
            </div>
          </div>

          {/* Total Orders */}
          <div className="rounded-2xl bg-purple-50/60 p-5 border border-purple-100 flex justify-between items-start transition hover:shadow-xs">
            <div>
              <p className="text-xs font-semibold text-purple-800">
                Total Orders
              </p>
              <h3 className="text-2xl font-bold text-slate-900 mt-2">8</h3>
              <button className="text-xs font-semibold text-purple-700 mt-2 flex items-center gap-1 group transition-colors">
                View your orders{" "}
                <ArrowRight className="h-3 w-3 transition-transform group-hover:translate-x-0.5" />
              </button>
            </div>
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-purple-100 text-purple-600">
              <ShoppingBag className="h-6 w-6" />
            </div>
          </div>
        </div>

        {/* 2. Middle Row: Wave Chart, Composition & Upcoming Pickup */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Smooth Wave Chart */}
          <SmoothWaveChart />

          {/* Donut Chart: Composition */}
          <div className="lg:col-span-3 rounded-2xl bg-white p-6 border border-slate-100 shadow-sm flex flex-col justify-between">
            <div>
              <h3 className="font-bold text-slate-900 mb-6">
                Waste Composition
              </h3>
              <div className="relative flex justify-center items-center my-4">
                <svg
                  className="w-36 h-36 transform -rotate-90"
                  viewBox="0 0 36 36"
                >
                  <path
                    className="text-emerald-500"
                    strokeDasharray="33, 100"
                    strokeWidth="4"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    className="text-amber-400"
                    strokeDasharray="18, 100"
                    strokeDashoffset="-33"
                    strokeWidth="4"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    className="text-indigo-400"
                    strokeDasharray="11, 100"
                    strokeDashoffset="-51"
                    strokeWidth="4"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    className="text-blue-500"
                    strokeDasharray="17, 100"
                    strokeDashoffset="-62"
                    strokeWidth="4"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                </svg>
                <div className="absolute text-center">
                  <span className="text-xl font-extrabold text-slate-900 block">
                    105
                  </span>
                  <span className="text-[10px] text-slate-400 font-bold uppercase">
                    kg
                  </span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-y-2 gap-x-1 text-xs text-slate-600 mt-6">
              <div className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-emerald-500" /> Organic
                33.3%
              </div>
              <div className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-blue-500" /> Paper
                17.1%
              </div>
              <div className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-amber-400" /> Glass
                11.4%
              </div>
              <div className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-indigo-400" /> Metal
                7.6%
              </div>
            </div>
          </div>

          {/* Upcoming Pickup Card */}
          <div className="lg:col-span-3 rounded-2xl bg-white p-6 border border-slate-100 shadow-sm flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-slate-900">Upcoming Pickup</h3>
                <span className="text-xs font-semibold text-emerald-600 hover:text-emerald-700 cursor-pointer">
                  View All
                </span>
              </div>

              <div className="rounded-xl bg-emerald-50/50 p-3.5 border border-emerald-100/60 mb-4 flex justify-between items-center">
                <div className="flex items-center gap-2.5">
                  <Calendar className="h-5 w-5 text-emerald-600" />
                  <div>
                    <p className="text-xs font-bold text-emerald-900">
                      Tomorrow, 28 July 2026
                    </p>
                    <p className="text-[11px] text-slate-500">
                      8:00 AM - 10:00 AM
                    </p>
                  </div>
                </div>
                <span className="text-[10px] font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-md">
                  #WP-7896
                </span>
              </div>

              <div className="space-y-3 text-xs text-slate-600">
                <div className="flex justify-between">
                  <span className="text-slate-400">Waste Type</span>
                  <span className="font-semibold text-slate-800">
                    Mixed Recyclables
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Quantity</span>
                  <span className="font-semibold text-slate-800">~ 10 kg</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">Collector</span>
                  <div className="flex items-center gap-1.5 font-semibold text-slate-800">
                    <img
                      src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80"
                      className="h-5 w-5 rounded-full object-cover"
                      alt="Jean Pierre"
                    />
                    Jean Pierre
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-400">Status</span>
                  <span className="bg-emerald-100 text-emerald-800 font-bold px-2 py-0.5 rounded-full text-[10px]">
                    Confirmed
                  </span>
                </div>
              </div>
            </div>

            <button className="w-full mt-5 rounded-xl bg-[#084127] py-2.5 text-xs font-semibold text-white hover:bg-emerald-900 transition-colors">
              View Pickup Details
            </button>
          </div>
        </div>

        {/* 3. NEW: COLLECTION HISTORY TABLE */}
        <div className="rounded-2xl bg-white border border-slate-100 shadow-sm p-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <div>
              <h3 className="font-bold text-slate-900 text-base">
                Recent Collection History
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Overview of your recent waste handovers, weights, and rewards
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button className="flex items-center gap-1.5 text-xs font-medium border border-slate-200 px-3 py-2 rounded-xl text-slate-600 hover:bg-slate-50 transition cursor-pointer">
                <Filter className="h-3.5 w-3.5 text-slate-500" /> Filter
              </button>
              <button className="flex items-center gap-1.5 text-xs font-medium border border-slate-200 px-3 py-2 rounded-xl text-slate-600 hover:bg-slate-50 transition cursor-pointer">
                <Download className="h-3.5 w-3.5 text-slate-500" /> Export
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-slate-50/80 text-slate-500 uppercase font-bold text-[10px] tracking-wider border-y border-slate-100">
                  <th className="py-3 px-4">Pickup ID</th>
                  <th className="py-3 px-4">Date & Time</th>
                  <th className="py-3 px-4">Category</th>
                  <th className="py-3 px-4">Weight</th>
                  <th className="py-3 px-4">Collector</th>
                  <th className="py-3 px-4">Points</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700 font-medium">
                {collectionHistory.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/80 transition">
                    <td className="py-3.5 px-4 font-bold text-slate-900">
                      {row.id}
                    </td>
                    <td className="py-3.5 px-4 text-slate-500 whitespace-nowrap">
                      {row.date} <span className="text-slate-300">|</span>{" "}
                      {row.time}
                    </td>
                    <td className="py-3.5 px-4 whitespace-nowrap">
                      <span
                        className={`border px-2.5 py-1 rounded-md text-[11px] font-semibold ${row.categoryBadge}`}
                      >
                        {row.category}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-semibold text-slate-800">
                      {row.weight}
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="flex items-center gap-2">
                        <img
                          src={row.avatar}
                          alt={row.collector}
                          className="h-5 w-5 rounded-full object-cover"
                        />
                        <span className="text-slate-800 font-semibold">
                          {row.collector}
                        </span>
                      </div>
                    </td>
                    <td className="py-3.5 px-4 font-bold text-emerald-600">
                      {row.points}
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`font-bold px-2.5 py-0.5 rounded-full text-[10px] ${row.statusBadge}`}
                      >
                        {row.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <button className="text-slate-400 hover:text-slate-600 p-1 rounded-md transition">
                        <MoreVertical className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 4. Bottom Row: Reward Levels, Summary & Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Reward Progress */}
          <div className="lg:col-span-5 rounded-2xl bg-white p-6 border border-slate-100 shadow-sm">
            <h3 className="font-bold text-slate-900 mb-1">Reward Progress</h3>
            <p className="text-xs text-slate-500 mb-4">
              Keep it up! You are{" "}
              <span className="font-bold text-emerald-600">65%</span> to the
              next level.
            </p>

            <div className="w-full bg-slate-100 h-2.5 rounded-full mb-6 overflow-hidden">
              <div className="bg-emerald-600 h-full rounded-full w-[65%]" />
            </div>

            <div className="grid grid-cols-4 gap-2 text-center">
              <div>
                <div className="h-12 w-12 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center mx-auto text-slate-400">
                  <Star className="h-5 w-5" />
                </div>
                <span className="text-xs font-bold text-slate-800 block mt-2">
                  Bronze
                </span>
                <span className="text-[10px] text-slate-400">0 - 1000 pts</span>
              </div>
              <div>
                <div className="h-12 w-12 rounded-full bg-emerald-700 text-white flex items-center justify-center mx-auto ring-4 ring-emerald-100">
                  <Star className="h-5 w-5 fill-white" />
                </div>
                <span className="text-xs font-bold text-slate-900 block mt-2">
                  Silver
                </span>
                <span className="text-[10px] text-slate-400">
                  1001 - 2500 pts
                </span>
              </div>
              <div>
                <div className="h-12 w-12 rounded-full bg-amber-50 border border-amber-200 text-amber-500 flex items-center justify-center mx-auto">
                  <Star className="h-5 w-5" />
                </div>
                <span className="text-xs font-bold text-slate-800 block mt-2">
                  Gold
                </span>
                <span className="text-[10px] text-slate-400">
                  2501 - 5000 pts
                </span>
              </div>
              <div>
                <div className="h-12 w-12 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center mx-auto text-slate-400">
                  <Star className="h-5 w-5" />
                </div>
                <span className="text-xs font-bold text-slate-800 block mt-2">
                  Platinum
                </span>
                <span className="text-[10px] text-slate-400">5001+ pts</span>
              </div>
            </div>
          </div>

          {/* Monthly Summary */}
          <div className="lg:col-span-4 rounded-2xl bg-white p-6 border border-slate-100 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-900">Monthly Summary</h3>
              <select className="text-xs font-medium border border-slate-200 rounded-lg px-2 py-1 bg-slate-50 text-slate-700 outline-none">
                <option>This Month</option>
              </select>
            </div>

            <div className="rounded-xl bg-blue-50/60 p-4 border border-blue-100 flex justify-between items-center mb-4">
              <div>
                <span className="text-xs font-semibold text-slate-600 block">
                  Collections
                </span>
                <span className="text-xl font-bold text-slate-900">5</span>
                <p className="text-[10px] font-medium text-emerald-600 mt-1">
                  +1 from last month ↑
                </p>
              </div>
              <div className="h-10 w-10 rounded-xl bg-blue-500 text-white flex items-center justify-center">
                <Truck className="h-5 w-5" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-xl bg-amber-50/60 p-3 border border-amber-100">
                <span className="text-[11px] font-semibold text-amber-900 block">
                  Points Earned
                </span>
                <span className="text-lg font-bold text-slate-900">350</span>
                <p className="text-[10px] font-medium text-emerald-600 mt-1">
                  +120 from last month
                </p>
              </div>
              <div className="rounded-xl bg-emerald-50/60 p-3 border border-emerald-100">
                <span className="text-[11px] font-semibold text-emerald-900 block">
                  CO₂ Saved
                </span>
                <span className="text-lg font-bold text-slate-900">
                  18.5 kg
                </span>
                <p className="text-[10px] font-medium text-emerald-600 mt-1">
                  +6.3 kg from last month
                </p>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="lg:col-span-3 rounded-2xl bg-white p-6 border border-slate-100 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-900">Recent Activity</h3>
              <span className="text-xs font-semibold text-emerald-600 cursor-pointer hover:text-emerald-700">
                View All
              </span>
            </div>

            <div className="space-y-4">
              <div className="flex gap-3">
                <div className="h-8 w-8 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0 mt-0.5">
                  <Recycle className="h-4 w-4" />
                </div>
                <div>
                  <h5 className="text-xs font-bold text-slate-800">
                    Pickup completed
                  </h5>
                  <p className="text-[10px] text-slate-500">
                    Your waste was collected successfully.
                  </p>
                  <span className="text-[9px] text-slate-400 block mt-0.5">
                    26 July 2026 • 09:15 AM
                  </span>
                </div>
              </div>

              <div className="flex gap-3">
                <div className="h-8 w-8 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center shrink-0 mt-0.5">
                  <Star className="h-4 w-4" />
                </div>
                <div>
                  <h5 className="text-xs font-bold text-slate-800">
                    You earned 120 points!
                  </h5>
                  <p className="text-[10px] text-slate-500">
                    Great job segregating your waste.
                  </p>
                  <span className="text-[9px] text-slate-400 block mt-0.5">
                    26 July 2026 • 09:20 AM
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 5. Bottom Community Banner */}
        <div className="rounded-2xl bg-emerald-50/80 p-4 border border-emerald-100 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-600 text-white shrink-0">
              <Truck className="h-5 w-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                Together, we build a cleaner Yaoundé VI{" "}
                <span className="text-emerald-600">💚</span>
              </h4>
              <p className="text-xs text-slate-500">
                Thank you for helping us make our community cleaner and greener.
              </p>
            </div>
          </div>
          <button className="rounded-xl bg-[#084127] px-5 py-2.5 text-xs font-semibold text-white hover:bg-emerald-900 transition-colors shrink-0">
            Learn More
          </button>
        </div>
      </div>
    </DashboardLayout>
  );
}
