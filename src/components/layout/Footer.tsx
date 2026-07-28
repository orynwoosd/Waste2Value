import { Mail, Phone, MapPin } from "lucide-react";
import { FaFacebook, FaInstagram, FaLinkedin, FaTwitter } from "react-icons/fa";

export default function Footer() {
  return (
    <footer id="contact" className="bg-gray-900 text-gray-300">
      <div className="mx-auto grid max-w-7xl gap-12 px-6 py-20 md:grid-cols-2 lg:grid-cols-4">
        {/* Brand */}
        <div>
          <h2 className="text-3xl font-bold text-white">Waste2Value</h2>

          <p className="mt-5 leading-7">
            Creating a cleaner and more sustainable future through smart waste
            recovery and recycling.
          </p>
        </div>

        {/* Quick Links */}
        <div>
          <h3 className="mb-5 text-lg font-semibold text-white">Quick Links</h3>

          <ul className="space-y-3">
            <li>
              <a href="#home">Home</a>
            </li>
            <li>
              <a href="#how-it-works">How It Works</a>
            </li>
            <li>
              <a href="#marketplace">Marketplace</a>
            </li>
            <li>
              <a href="#about">About</a>
            </li>
          </ul>
        </div>

        {/* Services */}
        <div>
          <h3 className="mb-5 text-lg font-semibold text-white">Services</h3>

          <ul className="space-y-3">
            <li>Waste Pickup</li>
            <li>Waste Recovery</li>
            <li>Recycling</li>
            <li>Rewards</li>
          </ul>
        </div>

        {/* Contact */}
        <div>
          <h3 className="mb-5 text-lg font-semibold text-white">Contact</h3>

          <div className="space-y-4">
            <div className="flex gap-3">
              <MapPin size={20} />
              <span>Yaoundé VI, Cameroon</span>
            </div>

            <div className="flex gap-3">
              <Mail size={20} />
              <span>support@waste2value.com</span>
            </div>

            <div className="flex gap-3">
              <Phone size={20} />
              <span>+237 830 545 95</span>
            </div>

            <div className="mt-6 flex gap-4">
              <FaFacebook className="cursor-pointer hover:text-green-500" />
              <FaInstagram className="cursor-pointer hover:text-green-500" />
              <FaLinkedin className="cursor-pointer hover:text-green-500" />
              <FaTwitter className="cursor-pointer hover:text-green-500" />
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-gray-700 py-6 text-center text-sm">
        © 2026 Waste2Value. All rights reserved.
      </div>
    </footer>
  );
}
