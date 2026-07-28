import { Star, ShoppingCart, Eye } from "lucide-react";

interface ProductCardProps {
  name: string;
  category: string;
  price: number;
  rating: number;
  image: string;
  onViewDetails?: () => void;
  onAddToCart?: () => void;
}

export default function ProductCard({
  name,
  category,
  price,
  rating,
  image,
  onViewDetails,
  onAddToCart,
}: ProductCardProps) {
  // Format price with commas (e.g., 15,000 FCFA)
  const formattedPrice = new Intl.NumberFormat().format(price);

  return (
    <div className="group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-gray-100 bg-white transition-all duration-300 hover:-translate-y-1.5 hover:border-gray-200 hover:shadow-xl hover:shadow-green-950/5">
      {/* Top Image Section */}
      <div className="relative aspect-[4/3] w-full overflow-hidden bg-gray-50">
        <img
          src={image}
          alt={name}
          className="h-full w-full object-cover object-center transition-transform duration-500 ease-out group-hover:scale-105"
        />

        {/* Category Pill Badge */}
        <span className="absolute left-3 top-3 rounded-full bg-white/90 px-3 py-1 text-xs font-medium text-gray-700 backdrop-blur-md shadow-sm">
          {category}
        </span>

        {/* Floating Quick View Action (Visible on Hover) */}
        <div className="absolute inset-0 flex items-center justify-center bg-black/20 opacity-0 transition-opacity duration-300 group-hover:opacity-100">
          <button
            onClick={onViewDetails}
            className="flex items-center gap-1.5 rounded-full bg-white px-4 py-2 text-xs font-semibold text-gray-900 shadow-md transition-transform hover:scale-105 active:scale-95"
          >
            <Eye size={14} />
            Quick View
          </button>
        </div>
      </div>

      {/* Card Content Section */}
      <div className="flex flex-1 flex-col justify-between p-5">
        <div className="space-y-2">
          {/* Rating & Review Count */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1">
              <Star size={15} className="fill-amber-400 text-amber-400" />
              <span className="text-xs font-semibold text-gray-700">
                {rating.toFixed(1)}
              </span>
            </div>
            <span className="text-xs text-gray-400">In Stock</span>
          </div>

          {/* Product Title */}
          <h3 className="line-clamp-1 text-base font-semibold text-gray-900 group-hover:text-green-600 transition-colors">
            {name}
          </h3>
        </div>

        {/* Pricing & Call to Action */}
        <div className="mt-4 flex items-center justify-between border-t border-gray-100 pt-3">
          <div>
            <span className="block text-[10px] uppercase tracking-wider text-gray-400">
              Price
            </span>
            <span className="text-lg font-bold text-gray-900">
              {formattedPrice}{" "}
              <span className="text-xs font-medium text-green-600">FCFA</span>
            </span>
          </div>

          {/* Cart Icon Button */}
          <button
            onClick={onAddToCart}
            aria-label="Add to cart"
            className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-50 text-green-700 transition-colors hover:bg-green-600 hover:text-white active:scale-95"
          >
            <ShoppingCart size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
