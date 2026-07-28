import { ArrowRight } from "lucide-react";

interface HeroSlideProps {
  image: string;
  title: string;
  description: string;
}

export default function HeroSlide({
  image,
  title,
  description,
}: HeroSlideProps) {
  return (
    <div className="relative flex min-h-screen w-full items-center justify-center">
      {/* Background Image */}
      <img
        src={image}
        alt={title}
        className="absolute inset-0 h-full w-full object-cover object-center scale-105 animate-pulse-subtle"
      />

      {/* Overlays for Readability */}
      {/* Top Gradient for Navbar Clarity */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/80 via-black/40 to-black/70" />

      {/* Subtle Radial Glow */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-green-900/20 via-transparent to-transparent" />

      {/* Slide Content */}
      <div className="relative z-10 mx-auto max-w-5xl px-6 pt-24 text-center">
        {/* Eco Badge */}

        {/* Title */}
        <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-6xl md:text-7xl leading-tight">
          {title}
        </h1>

        {/* Description */}
        <p className="mx-auto mt-6 max-w-2xl text-base text-gray-200 sm:text-lg md:text-xl font-light leading-relaxed">
          {description}
        </p>

        {/* CTA Buttons */}
        <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a
            href="#marketplace"
            className="group relative flex items-center justify-center gap-2 overflow-hidden rounded-xl bg-green-600 px-7 py-3.5 text-sm font-semibold text-white shadow-lg shadow-green-600/30 transition-all duration-300 hover:bg-green-500 hover:shadow-xl hover:shadow-green-600/40 active:scale-95"
          >
            Explore Marketplace
            <ArrowRight
              size={18}
              className="transition-transform duration-300 group-hover:translate-x-1"
            />
          </a>

          <a
            href="#how-it-works"
            className="flex items-center justify-center gap-2 rounded-xl border border-white/20 bg-white/10 px-7 py-3.5 text-sm font-semibold text-white backdrop-blur-md transition-all duration-300 hover:bg-white/20 hover:border-white/40 active:scale-95"
          >
            Learn How It Works
          </a>
        </div>
      </div>
    </div>
  );
}
