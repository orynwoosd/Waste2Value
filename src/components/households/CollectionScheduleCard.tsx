import React from "react";
import { Calendar, Truck, Clock } from "lucide-react";
import type { PickupSchedule } from "./types";

interface Props {
  pickups: PickupSchedule[];
  onSchedulePickup?: () => void;
}

const statusBadges = {
  scheduled:
    "bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 border-blue-200",
  "in-transit":
    "bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300 border-amber-200",
  completed:
    "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border-emerald-200",
  cancelled:
    "bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 border-rose-200",
};

export const CollectionScheduleCard: React.FC<Props> = ({
  pickups,
  onSchedulePickup,
}) => {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-slate-900 dark:text-white flex items-center gap-2">
          <Truck className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          Upcoming Pickups
        </h3>
        {onSchedulePickup && (
          <button
            onClick={onSchedulePickup}
            className="text-xs font-medium text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800 rounded-lg px-3 py-1.5 hover:bg-emerald-50 dark:hover:bg-emerald-950/30 transition-colors"
          >
            + Request Pickup
          </button>
        )}
      </div>

      {pickups.length === 0 ? (
        <p className="text-sm text-slate-500 py-4 text-center">
          No upcoming waste pickups scheduled.
        </p>
      ) : (
        <div className="space-y-3">
          {pickups.map((pickup) => (
            <div
              key={pickup.id}
              className="flex items-center justify-between p-3 rounded-lg border border-slate-100 dark:border-slate-700/60 bg-slate-50/50 dark:bg-slate-800/50"
            >
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-md bg-white dark:bg-slate-700 shadow-xs">
                  <Calendar className="w-4 h-4 text-slate-600 dark:text-slate-300" />
                </div>
                <div>
                  <p className="text-sm font-semibold capitalize text-slate-900 dark:text-white">
                    {pickup.category} Waste
                  </p>
                  <p className="text-xs text-slate-500 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {pickup.scheduledDate} • {pickup.timeSlot}
                  </p>
                </div>
              </div>
              <span
                className={`text-xs px-2.5 py-1 rounded-full font-medium border ${statusBadges[pickup.status]}`}
              >
                {pickup.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
