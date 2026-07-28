export type WasteCategory = 'plastic' | 'organic' | 'paper' | 'glass' | 'e-waste';

export interface WasteCategorySummary {
  category: WasteCategory;
  weightKg: number;
  colorClass: string;
}

export interface PickupSchedule {
  id: string;
  category: WasteCategory;
  scheduledDate: string;
  timeSlot: string;
  status: 'scheduled' | 'in-transit' | 'completed' | 'cancelled';
  collectorName?: string;
}

export interface WasteRecord {
  id: string;
  date: string;
  category: WasteCategory;
  weightKg: number;
  pointsEarned: number;
  monetaryValue: number;
  status: 'verified' | 'pending';
}

export interface HouseholdStats {
  householdId: string;
  householdName: string;
  address: string;
  totalRecycledKg: number;
  totalRewardPoints: number;
  co2SavedKg: number;
  monthlyTargetKg: number;
}