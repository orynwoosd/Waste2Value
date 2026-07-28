import Navbar from "../../components/layout/Navbar";
import Hero from "../../components/home/Hero";
import HowItWorks from "../../components/home/HowItWorks";
import Statistics from "../../components/home/Statistics";
import MarketplacePreview from "../../components/home/Marketplace/MarketplacePreview";
import About from "../../components/home/About";
import CallToAction from "../../components/home/CallToAction";
import Footer from "../../components/layout/Footer";

export default function Home() {
  return (
    <>
      <Navbar />

      <main>
        <Hero />
        <Statistics />
        <HowItWorks />
        <MarketplacePreview />
        <About />
        <CallToAction />
      </main>

      <Footer />
    </>
  );
}
