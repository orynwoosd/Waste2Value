import React from "react";
import { Recycle, CheckCircle2, Clock } from "lucide-react";
import type { WasteRecord } from "./types";

interface Props {
  records: WasteRecord[];
}

export const RecentPickupsTable: React.FC<Props> = ({ records }) => {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden shadow-sm">
      <div className="p-5 border-b border-slate-200 dark:border-slate-700 flex justify-between items-center">
        <h3 className="font-semibold text-slate-900 dark:text-white flex items-center gap-2">
          <Recycle className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          Recent Recycled Waste Ledger
        </h3>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 dark:bg-slate-900/50 text-xs text-slate-500 dark:text-slate-400 border-b border-slate-200 dark:border-slate-700">
              <th className="p-3.5 pl-5">Date</th>
              <th className="p-3.5">Category</th>
              <th className="p-3.5">Weight</th>
              <th className="p-3.5">Points Earned</th>
              <th className="p-3.5">Estimated Value</th>
              <th className="p-3.5 pr-5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200 dark:divide-slate-700/60 text-sm">
            {records.map((item) => (
              <tr
                key={item.id}
                className="hover:bg-slate-50/80 dark:hover:bg-slate-700/30 transition-colors"
              >
                <td className="p-3.5 pl-5 font-medium text-slate-900 dark:text-white">
                  {item.date}
                </td>
                <td className="p-3.5 capitalize text-slate-700 dark:text-slate-300">
                  {item.category}
                </td>
                <td className="p-3.5 font-semibold text-slate-900 dark:text-white">
                  {item.weightKg} kg
                </td>
                <td className="p-3.5 font-medium text-emerald-600 dark:text-emerald-400">
                  +{item.pointsEarned} pts
                </td>
                <td className="p-3.5 text-slate-700 dark:text-slate-300">
                  ${item.monetaryValue.toFixed(2)}
                </td>
                <td className="p-3.5 pr-5">
                  {item.status === "verified" ? (
                    <span className="inline-flex items-center gap-1 text-xs text-emerald-600 dark:text-emerald-400 font-medium">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Verified
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-xs text-amber-600 dark:text-amber-400 font-medium">
                      <Clock className="w-3.5 h-3.5" /> Pending Weigh
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
