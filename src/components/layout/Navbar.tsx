import { useEffect, useState } from "react";
import { Menu, X, ChevronDown, Globe } from "lucide-react";
import logo from "../../assets/images/logo.jpeg";

const navLinks = [
  { name: "Home", href: "#home" },
  { name: "How It Works", href: "#how-it-works" },
  { name: "Our Impact", href: "#impact" },
  { name: "Marketplace", href: "#marketplace" },
  { name: "About Us", href: "#about" },
  { name: "Contact", href: "#contact" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [activeSection, setActiveSection] = useState("home");
  const [langOpen, setLangOpen] = useState(false);
  const [selectedLang, setSelectedLang] = useState("EN");

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);

      const sections = navLinks.map((link) => link.href.substring(1));
      const scrollPosition = window.scrollY + 100;

      for (const section of sections) {
        const element = document.getElementById(section);
        if (element) {
          const top = element.offsetTop;
          const height = element.offsetHeight;
          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveSection(section);
            break;
          }
        }
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-white/80 py-3.5 shadow-sm backdrop-blur-md border-b border-gray-100"
          : "bg-transparent py-5"
      }`}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6">
        {/* Brand Logo with Image */}
        <a
          href="#home"
          className="group flex items-center gap-2.5 text-2xl font-bold tracking-tight"
        >
          {/* 2. Replaced text "logo" with real <img> tag */}
          <img
            src={logo}
            alt="Waste2Value Logo"
            className="h-9 w-9 rounded-xl object-cover shadow-md transition-transform duration-300 group-hover:scale-105"
          />

          <span
            className={`transition-colors duration-300 ${
              scrolled ? "text-gray-900" : "text-white"
            }`}
          >
            Waste<span className="text-green-600">2Value</span>
          </span>
        </a>

        {/* Desktop Navigation Links */}
        <nav className="hidden items-center gap-1 rounded-full bg-black/5 p-1.5 backdrop-blur-sm lg:flex border border-white/10">
          {navLinks.map((link) => {
            const isActive = activeSection === link.href.substring(1);
            return (
              <a
                key={link.name}
                href={link.href}
                className={`relative px-4 py-2 text-sm font-medium transition-all duration-200 ${
                  scrolled
                    ? isActive
                      ? "text-green-600 font-semibold"
                      : "text-gray-600 hover:text-gray-900"
                    : isActive
                      ? "text-white font-semibold"
                      : "text-white/80 hover:text-white"
                }`}
              >
                {link.name}

                {/* Active Indicator Bar */}
                <span
                  className={`absolute inset-x-3 -bottom-1 h-0.5 rounded-full bg-green-500 transition-all duration-300 ${
                    isActive
                      ? "opacity-100 scale-x-100"
                      : "opacity-0 scale-x-0 group-hover:opacity-100 group-hover:scale-x-100"
                  }`}
                />
              </a>
            );
          })}
        </nav>

        {/* Right Actions */}
        <div className="hidden items-center gap-3 lg:flex">
          <div className="relative">
            <button
              onClick={() => setLangOpen(!langOpen)}
              className={`flex items-center gap-1.5 rounded-lg px-3 py-2 text-xs font-semibold tracking-wider transition ${
                scrolled
                  ? "text-gray-700 hover:bg-gray-100"
                  : "text-white hover:bg-white/10"
              }`}
            >
              <Globe size={15} />
              {selectedLang}
              <ChevronDown
                size={14}
                className={`transition-transform duration-200 ${
                  langOpen ? "rotate-180" : ""
                }`}
              />
            </button>

            {langOpen && (
              <div className="absolute right-0 mt-2 w-28 overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl animate-in fade-in zoom-in-95 duration-150">
                <button
                  onClick={() => {
                    setSelectedLang("EN");
                    setLangOpen(false);
                  }}
                  className="block w-full px-4 py-2.5 text-left text-xs font-medium text-gray-700 hover:bg-green-50 hover:text-green-600"
                >
                  English (EN)
                </button>
                <button
                  onClick={() => {
                    setSelectedLang("FR");
                    setLangOpen(false);
                  }}
                  className="block w-full px-4 py-2.5 text-left text-xs font-medium text-gray-700 hover:bg-green-50 hover:text-green-600"
                >
                  Français (FR)
                </button>
              </div>
            )}
          </div>

          <button
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition-all active:scale-95 ${
              scrolled
                ? "text-gray-700 hover:bg-gray-100"
                : "text-white hover:bg-white/10"
            }`}
          >
            Sign In
          </button>

          <button className="relative group overflow-hidden rounded-xl bg-green-600 px-5 py-2.5 text-sm font-semibold text-white shadow-md shadow-green-600/20 transition-all duration-300 hover:bg-green-700 hover:shadow-lg hover:shadow-green-600/30 active:scale-95">
            <span className="relative z-10">Get Started</span>
          </button>
        </div>

        {/* Mobile Menu Button */}
        <button
          className={`rounded-xl p-2 transition lg:hidden ${
            scrolled
              ? "text-gray-800 hover:bg-gray-100"
              : "text-white hover:bg-white/10"
          }`}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle navigation menu"
        >
          {isOpen ? <X size={26} /> : <Menu size={26} />}
        </button>
      </div>

      {/* Mobile Drawer Navigation */}
      {isOpen && (
        <div className="absolute inset-x-0 top-full border-b border-gray-100 bg-white px-6 py-6 shadow-2xl transition-all duration-300 lg:hidden">
          <nav className="flex flex-col space-y-1">
            {navLinks.map((link) => (
              <a
                key={link.name}
                href={link.href}
                className="rounded-xl px-4 py-3 text-base font-medium text-gray-700 transition hover:bg-green-50 hover:text-green-600"
                onClick={() => setIsOpen(false)}
              >
                {link.name}
              </a>
            ))}
          </nav>

          <div className="mt-6 flex flex-col gap-3 border-t border-gray-100 pt-5">
            <button className="w-full rounded-xl border border-gray-200 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50 active:scale-98">
              Sign In
            </button>
            <button className="w-full rounded-xl bg-green-600 py-3 text-sm font-semibold text-white shadow-md shadow-green-600/20 hover:bg-green-700 active:scale-98">
              Get Started
            </button>
          </div>
        </div>
      )}
    </header>
  );
}
