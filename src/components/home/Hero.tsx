import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay, Pagination, EffectFade } from "swiper/modules";

import "swiper/css";
import "swiper/css/effect-fade";
import "swiper/css/pagination";

import HeroSlide from "./HeroSlide";
import { slides } from "./slides";

export default function Hero() {
  return (
    <section
      id="home"
      className="relative min-h-screen w-full overflow-hidden bg-gray-900"
    >
      <Swiper
        modules={[Autoplay, Pagination, EffectFade]}
        effect="fade"
        speed={1000}
        autoplay={{
          delay: 6000,
          disableOnInteraction: false,
        }}
        pagination={{
          clickable: true,
          renderBullet: (_, className) => {
            return `<span class="${className} custom-bullet"></span>`;
          },
        }}
        loop
        className="h-full min-h-screen w-full"
      >
        {slides.map((slide) => (
          <SwiperSlide key={slide.id} className="h-full min-h-screen">
            <HeroSlide
              image={slide.image}
              title={slide.title}
              description={slide.description}
            />
          </SwiperSlide>
        ))}
      </Swiper>

      {/* Custom Swiper Pagination Styling Overlay */}
      <style>{`
        .swiper-pagination {
          bottom: 2.5rem !important;
          display: flex;
          justify-content: center;
          gap: 0.5rem;
        }
        .swiper-pagination-bullet {
          width: 0.75rem;
          height: 0.75rem;
          background: rgba(255, 255, 255, 0.4);
          opacity: 1;
          transition: all 0.3s ease;
          border-radius: 9999px;
        }
        .swiper-pagination-bullet-active {
          width: 2.25rem;
          background: #22c55e !important;
        }
      `}</style>
    </section>
  );
}
