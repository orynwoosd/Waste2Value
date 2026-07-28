import { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Trash2,
  CreditCard,
  Wallet,
  ShoppingBag,
  Bell,
  Settings,
  ChevronDown,
  Recycle,
  CalendarDays,
  History,
  Store,
  ShoppingCart,
  PackageCheck,
  User,
  Sparkles,
} from "lucide-react";

export default function Sidebar() {
  const [pickupOpen, setPickupOpen] = useState(true);
  const [marketOpen, setMarketOpen] = useState(false);

  // Styling helper for top-level navigation links
  const linkClasses = ({ isActive }: { isActive: boolean }) =>
    `relative flex items-center gap-3.5 rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200 ${
      isActive
        ? "bg-white text-[#084127] font-bold shadow-lg shadow-black/10 scale-[1.02] before:absolute before:-left-1 before:top-2.5 before:h-7 before:w-1.5 before:rounded-r-full before:bg-emerald-400"
        : "text-emerald-100/80 hover:bg-emerald-800/40 hover:text-white"
    }`;

  // Styling helper for nested sub-menu links
  const subLinkClasses = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-2.5 rounded-lg px-3 py-2 text-xs font-medium transition-all duration-200 ${
      isActive
        ? "bg-emerald-500/20 text-white font-semibold"
        : "text-emerald-200/70 hover:bg-emerald-800/30 hover:text-white"
    }`;

  return (
    <aside className="fixed left-0 top-0 flex h-screen w-[270px] flex-col bg-[#084127] shadow-2xl z-30 select-none">
      {/* ================= LOGO & BRANDING ================= */}
      <div className="border-b border-emerald-900/60 px-6 py-5">
        <div className="flex items-center gap-3.5">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white shadow-md shadow-emerald-950/20">
            <Recycle className="h-6 w-6 text-[#084127] stroke-[2.5]" />
          </div>

          <div>
            <h1 className="text-lg font-bold tracking-tight text-white leading-tight">
              Waste2Value
            </h1>
            <p className="text-[11px] font-medium text-emerald-300/90">
              Recycle Today, Green Tomorrow
            </p>
          </div>
        </div>
      </div>

      {/* ================= MENU NAVIGATION ================= */}
      <nav className="flex-1 overflow-y-auto px-4 py-5 scrollbar-thin scrollbar-thumb-emerald-800/40">
        <div className="space-y-1.5">
          {/* Dashboard */}
          <NavLink to="/household/dashboard" className={linkClasses}>
            <LayoutDashboard size={19} />
            <span>Dashboard</span>
          </NavLink>

          {/* WASTE PICKUP ACCORDION */}
          <div>
            <button
              onClick={() => setPickupOpen(!pickupOpen)}
              className={`flex w-full items-center justify-between rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200 ${
                pickupOpen
                  ? "text-white bg-emerald-900/30"
                  : "text-emerald-100/80 hover:bg-emerald-800/40 hover:text-white"
              }`}
            >
              <div className="flex items-center gap-3.5">
                <Trash2 size={19} />
                <span>Waste Pickup</span>
              </div>

              <ChevronDown
                size={16}
                className={`transition-transform duration-300 text-emerald-300 ${
                  pickupOpen ? "rotate-180" : ""
                }`}
              />
            </button>

            <div
              className={`overflow-hidden transition-all duration-300 ease-in-out ${
                pickupOpen ? "max-h-40 opacity-100 mt-1" : "max-h-0 opacity-0"
              }`}
            >
              <div className="ml-5 border-l-2 border-emerald-700/50 pl-3 space-y-1">
                <NavLink
                  to="/household/schedule-pickup"
                  className={subLinkClasses}
                >
                  <CalendarDays size={15} />
                  <span>Schedule Pickup</span>
                </NavLink>

                <NavLink
                  to="/household/pickup-history"
                  className={subLinkClasses}
                >
                  <History size={15} />
                  <span>Pickup History</span>
                </NavLink>
              </div>
            </div>
          </div>

          {/* SUBSCRIPTIONS */}
          <NavLink to="/household/subscriptions" className={linkClasses}>
            <CreditCard size={19} />
            <span>Subscriptions</span>
          </NavLink>

          {/* REWARDS & WALLET */}
          <NavLink to="/household/rewards" className={linkClasses}>
            <Wallet size={19} />
            <span>Rewards & Wallet</span>
          </NavLink>

          {/* MARKETPLACE ACCORDION */}
          <div>
            <button
              onClick={() => setMarketOpen(!marketOpen)}
              className={`flex w-full items-center justify-between rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200 ${
                marketOpen
                  ? "text-white bg-emerald-900/30"
                  : "text-emerald-100/80 hover:bg-emerald-800/40 hover:text-white"
              }`}
            >
              <div className="flex items-center gap-3.5">
                <ShoppingBag size={19} />
                <span>Marketplace</span>
              </div>

              <ChevronDown
                size={16}
                className={`transition-transform duration-300 text-emerald-300 ${
                  marketOpen ? "rotate-180" : ""
                }`}
              />
            </button>

            <div
              className={`overflow-hidden transition-all duration-300 ease-in-out ${
                marketOpen ? "max-h-56 opacity-100 mt-1" : "max-h-0 opacity-0"
              }`}
            >
              <div className="ml-5 border-l-2 border-emerald-700/50 pl-3 space-y-1">
                <NavLink to="/household/marketplace" className={subLinkClasses}>
                  <Store size={15} />
                  <span>Browse Products</span>
                </NavLink>

                <NavLink to="/household/categories" className={subLinkClasses}>
                  <ShoppingBag size={15} />
                  <span>Categories</span>
                </NavLink>

                <NavLink to="/household/cart" className={subLinkClasses}>
                  <ShoppingCart size={15} />
                  <span>Cart</span>
                </NavLink>

                <NavLink to="/household/orders" className={subLinkClasses}>
                  <PackageCheck size={15} />
                  <span>My Orders</span>
                </NavLink>
              </div>
            </div>
          </div>

          {/* NOTIFICATIONS */}
          <NavLink to="/household/notifications" className={linkClasses}>
            <Bell size={19} />
            <span className="flex-1">Notifications</span>
            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-amber-400 text-[11px] font-bold text-slate-900 shadow-sm">
              3
            </span>
          </NavLink>

          {/* PROFILE & SETTINGS */}
          <NavLink to="/household/settings" className={linkClasses}>
            <Settings size={19} />
            <span>Profile & Settings</span>
          </NavLink>
        </div>
      </nav>

      {/* ================= PROMO CARD ================= */}
      <div className="px-4 pb-3">
        <div className="relative overflow-hidden rounded-2xl border border-emerald-600/30 bg-gradient-to-br from-[#0d4d30] to-[#073620] p-4 text-left shadow-inner">
          <div className="flex items-center gap-1.5 text-amber-300 mb-1">
            <Sparkles size={14} />
            <span className="text-[10px] font-bold uppercase tracking-wider">
              Eco Bonus
            </span>
          </div>

          <h3 className="text-xs font-bold text-white">Segregate Waste</h3>

          <p className="mt-1 text-[11px] leading-relaxed text-emerald-200/80">
            Keep separating recyclable waste and earn more reward points every
            pickup.
          </p>

          <div className="mt-3 flex justify-center">
            <img
              src="/illustrations/recycle-banner.png"
              alt="Recycle Illustration"
              className="h-20 w-auto object-contain drop-shadow-md"
              onError={(e) => {
                // Smooth fallback in case illustration file is missing
                (e.target as HTMLElement).style.display = "none";
              }}
            />
          </div>
        </div>
      </div>

      {/* ================= USER FOOTER ================= */}
      <div className="border-t border-emerald-900/60 px-5 py-4 bg-emerald-950/40">
        <div className="flex items-center gap-3">
          <div className="relative flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-emerald-500 to-emerald-700 shadow-sm border border-emerald-400/30">
            <User size={18} className="text-white" />
            <span className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full bg-emerald-400 ring-2 ring-[#084127]" />
          </div>

          <div className="overflow-hidden">
            <h4 className="text-xs font-bold text-white truncate">
              Fru Patience
            </h4>
            <p className="text-[11px] font-medium text-emerald-300/80 truncate">
              Household Member
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
