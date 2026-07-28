import { useState } from "react";
import { ArrowRight, ShoppingBag, Sparkles } from "lucide-react";
import ProductCard from "./ProductCard";
import { products } from "./Products";

// Dynamic categories extracted automatically from products
const categories = ["All", "Fertilizer", "Gardening", "Construction"];

export default function MarketplacePreview() {
  const [activeCategory, setActiveCategory] = useState("All");

  // Filter products based on selected tab
  const filteredProducts =
    activeCategory === "All"
      ? products
      : products.filter(
          (product) =>
            product.category.toLowerCase() === activeCategory.toLowerCase(),
        );

  return (
    <section
      id="marketplace"
      className="relative overflow-hidden bg-slate-50/60 py-24"
    >
      {/* Background Decorative Ambient Blur */}
      <div className="absolute -left-20 top-1/2 h-72 w-72 rounded-full bg-green-200/40 blur-3xl pointer-events-none" />

      <div className="relative mx-auto max-w-7xl px-6">
        {/* Header Section */}
        <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between mb-12">
          <div className="max-w-2xl">
            {/* Pill Badge */}
            <span className="inline-flex items-center gap-1.5 rounded-full bg-green-100 px-3.5 py-1 text-xs font-semibold uppercase tracking-wider text-green-800">
              <Sparkles size={14} />
              Sustainable Store
            </span>

            <h2 className="mt-4 text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl lg:text-5xl">
              Products Made from{" "}
              <span className="text-green-600">Recycled Waste</span>
            </h2>

            <p className="mt-4 text-base text-gray-600 font-light sm:text-lg">
              Browse high-quality products created from recovered waste
              materials, supporting sustainability while giving valuable
              resources a second life.
            </p>
          </div>

          {/* Top CTA Button */}
          <a
            href="/marketplace"
            className="group inline-flex items-center justify-center gap-2 rounded-xl bg-green-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-green-600/20 transition-all duration-300 hover:bg-green-700 hover:shadow-xl hover:shadow-green-600/30 active:scale-95 shrink-0"
          >
            <ShoppingBag size={18} />
            Explore Full Shop
            <ArrowRight
              size={16}
              className="transition-transform group-hover:translate-x-1"
            />
          </a>
        </div>

        {/* Category Filter Tabs */}
        <div className="flex flex-wrap items-center gap-2 mb-10 border-b border-gray-200/80 pb-4">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setActiveCategory(category)}
              className={`rounded-xl px-4 py-2 text-xs font-semibold transition-all duration-200 ${
                activeCategory === category
                  ? "bg-green-600 text-white shadow-md shadow-green-600/20"
                  : "bg-white text-gray-600 hover:bg-gray-100 hover:text-gray-900 border border-gray-200/60"
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Product Cards Grid */}
        {filteredProducts.length > 0 ? (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {filteredProducts.map((product) => (
              <ProductCard key={product.id} {...product} />
            ))}
          </div>
        ) : (
          /* Empty State if no products match selected filter */
          <div className="rounded-2xl border border-dashed border-gray-200 bg-white p-12 text-center">
            <p className="text-sm font-medium text-gray-500">
              No products found in the "{activeCategory}" category.
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
