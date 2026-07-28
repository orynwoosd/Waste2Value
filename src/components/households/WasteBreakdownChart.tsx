import React from "react";
import { PieChart, Layers } from "lucide-react";
import type { WasteCategory, WasteCategorySummary } from "./types";

interface WasteBreakdownChartProps {
  categoriesSummary: WasteCategorySummary[];
  timeframeLabel?: string;
}

const defaultCategoryConfig: Record<
  WasteCategory,
  { label: string; defaultColor: string }
> = {
  plastic: { label: "Plastics & Polymers", defaultColor: "bg-indigo-500" },
  organic: { label: "Organic Compost", defaultColor: "bg-emerald-500" },
  paper: { label: "Paper & Cardboard", defaultColor: "bg-amber-500" },
  glass: { label: "Glass Containers", defaultColor: "bg-sky-500" },
  "e-waste": { label: "Electronic Waste", defaultColor: "bg-rose-500" },
};

export const WasteBreakdownChart: React.FC<WasteBreakdownChartProps> = ({
  categoriesSummary,
  timeframeLabel = "This Month",
}) => {
  const totalWeightKg = categoriesSummary.reduce(
    (acc, item) => acc + item.weightKg,
    0,
  );

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/80 p-5 shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="font-semibold text-slate-900 dark:text-white flex items-center gap-2">
            <PieChart className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            Waste Segregation Breakdown
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Material distribution ({timeframeLabel})
          </p>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-500 dark:text-slate-400 block">
            Total Recycled
          </span>
          <span className="text-base font-bold text-slate-900 dark:text-white">
            {totalWeightKg.toFixed(1)} kg
          </span>
        </div>
      </div>

      {/* Stacked Bar */}
      <div className="mb-6">
        <div className="w-full h-3.5 bg-slate-100 dark:bg-slate-700/60 rounded-full overflow-hidden flex">
          {categoriesSummary.map((item) => {
            const percentage =
              totalWeightKg > 0 ? (item.weightKg / totalWeightKg) * 100 : 0;

            if (percentage === 0) return null;

            const config = defaultCategoryConfig[item.category];
            const barColor = item.colorClass || config.defaultColor;

            return (
              <div
                key={item.category}
                style={{ width: `${percentage}%` }}
                className={`h-full transition-all duration-500 ${barColor}`}
                title={`${config.label}: ${item.weightKg} kg (${percentage.toFixed(1)}%)`}
              />
            );
          })}
        </div>
      </div>

      {/* Categorized Progress List */}
      <div className="space-y-3.5">
        {categoriesSummary.map((item) => {
          const config = defaultCategoryConfig[item.category];
          const percentage =
            totalWeightKg > 0
              ? Math.round((item.weightKg / totalWeightKg) * 100)
              : 0;
          const barColor = item.colorClass || config.defaultColor;

          return (
            <div key={item.category} className="space-y-1">
              <div className="flex justify-between items-center text-xs">
                <div className="flex items-center gap-2">
                  <span className={`w-2.5 h-2.5 rounded-full ${barColor}`} />
                  <span className="font-medium text-slate-700 dark:text-slate-300">
                    {config.label}
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="font-semibold text-slate-900 dark:text-white">
                    {item.weightKg} kg
                  </span>
                  <span className="text-slate-400 dark:text-slate-500 w-8 text-right">
                    {percentage}%
                  </span>
                </div>
              </div>

              <div className="w-full h-1.5 bg-slate-100 dark:bg-slate-700/50 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-300 ${barColor}`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Footnote */}
      <div className="mt-5 pt-3 border-t border-slate-100 dark:border-slate-700/60 flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
        <Layers className="w-4 h-4 text-emerald-500 shrink-0" />
        <span>
          Higher plastic and e-waste segregation yields bonus reward
          multipliers.
        </span>
      </div>
    </div>
  );
};
