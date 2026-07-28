import React from "react";
import { Bell, ChevronDown, Menu, Search, Wallet, Star } from "lucide-react";

interface TopbarProps {
  onMenuClick?: () => void;
}

export default function Topbar({ onMenuClick }: TopbarProps) {
  const now = new Date();
  const hour = now.getHours();

  const greeting =
    hour < 12 ? "Good Morning" : hour < 18 ? "Good Afternoon" : "Good Evening";

  const today = now.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });

  return (
    <header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-slate-200/80 bg-white/90 px-6 lg:px-8 backdrop-blur-md">
      {/* ================= LEFT SECTION: GREETING & DATE ================= */}
      <div className="flex items-center gap-4">
        {/* Mobile Navigation Toggle Button */}
        <button
          onClick={onMenuClick}
          className="flex h-10 w-10 items-center justify-center rounded-xl text-slate-600 transition-colors hover:bg-slate-100/80 active:scale-95 lg:hidden"
          aria-label="Open Navigation Menu"
        >
          <Menu className="h-6 w-6" />
        </button>

        <div>
          <h1 className="text-lg lg:text-xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
            {greeting}, Ndeusse Family{" "}
          </h1>

          <p className="text-xs text-slate-500 font-medium">
            {today}{" "}
            <span className="hidden sm:inline text-slate-400">
              • Let's make Yaoundé cleaner today.
            </span>
          </p>
        </div>
      </div>

      {/* ================= RIGHT SECTION: ACTIONS & METRICS ================= */}
      <div className="flex items-center gap-3 lg:gap-4">
        {/* Search Bar */}
        <div className="hidden xl:flex">
          <div className="group flex items-center gap-3 rounded-full border border-slate-200 bg-slate-50/80 px-4 py-2 text-xs transition-all duration-200 focus-within:border-emerald-500 focus-within:bg-white focus-within:ring-4 focus-within:ring-emerald-500/10">
            <Search className="h-4 w-4 text-slate-400 group-focus-within:text-emerald-600 transition-colors" />
            <input
              type="text"
              placeholder="Search products, pickups..."
              className="w-52 bg-transparent text-slate-800 outline-none placeholder:text-slate-400 font-medium"
            />
          </div>
        </div>

        {/* Notifications Icon Button */}
        <button
          className="relative flex h-10 w-10 items-center justify-center rounded-2xl border border-slate-200/80 bg-white shadow-2xs transition-all duration-200 hover:bg-slate-50 hover:border-slate-300 active:scale-95"
          aria-label="Notifications"
        >
          <Bell className="h-4 w-4 text-slate-600" />
          <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-amber-400 text-[10px] font-bold text-slate-900 shadow-xs ring-2 ring-white">
            3
          </span>
        </button>

        {/* User Profile Pill Button */}
        <button className="group flex items-center gap-2.5 rounded-full border border-slate-200/80 bg-white p-1 pr-3.5 shadow-2xs transition-all duration-200 hover:bg-slate-50 hover:border-slate-300">
          <div className="relative">
            <img
              src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200"
              alt="Ndeusse Family"
              className="h-8 w-8 rounded-full object-cover ring-1 ring-slate-200"
            />
            <span className="absolute bottom-0 right-0 h-2 w-2 rounded-full bg-emerald-500 ring-2 ring-white" />
          </div>

          <div className="hidden text-left md:block">
            <h4 className="text-xs font-bold text-slate-900 leading-tight">
              Ndeusse Family
            </h4>
            <p className="text-[10px] font-medium text-slate-400">
              Household Member
            </p>
          </div>

          <ChevronDown className="h-3.5 w-3.5 text-slate-400 transition-transform duration-200 group-hover:translate-y-0.5" />
        </button>
      </div>
    </header>
  );
}
