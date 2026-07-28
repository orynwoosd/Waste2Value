import type { ReactNode } from "react";
import AccountSidebar from "../../components/auth/AccountSidebar";

interface RegisterLayoutProps {
  children: ReactNode;
}

export default function RegisterLayout({ children }: RegisterLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-8">
      <div className="w-full max-w-7xl bg-white rounded-3xl shadow-xl overflow-hidden grid lg:grid-cols-3">
        <AccountSidebar />

        <div className="lg:col-span-2 p-12">{children}</div>
      </div>
    </div>
  );
}
