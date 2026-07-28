const steps = [
  { number: 1, title: "Register", desc: "Create your household account" },
  { number: 2, title: "Segregate Waste", desc: "Separate your waste properly" },
  { number: 3, title: "Request Pickup", desc: "Schedule a pickup" },
  { number: 4, title: "We Collect", desc: "Collectors come to you" },
  { number: 5, title: "Earn Rewards", desc: "Redeem exciting rewards" },
];

export default function HowItWorks() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-4xl font-bold">
            How <span className="text-green-700">Waste2Value</span> Works
          </h2>
          <p className="text-gray-600 mt-3">
            Five simple steps to managing your domestic waste cleanly and
            earning benefits.
          </p>
        </div>

        <div className="grid md:grid-cols-5 gap-8 relative">
          {steps.map((step, index) => (
            <div
              key={step.number}
              className="text-center relative z-10 flex flex-col items-center"
            >
              {/* Connector line for desktop */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-6 left-1/2 w-full h-0.5 bg-green-200 -z-10" />
              )}

              <div className="w-12 h-12 rounded-full bg-green-700 text-white flex items-center justify-center font-bold text-lg shadow-md mb-4 ring-4 ring-white">
                {step.number}
              </div>

              <h3 className="font-semibold text-gray-900">{step.title}</h3>
              <p className="text-gray-500 text-sm mt-2 leading-relaxed">
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
