import { lazy, Suspense } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, Sparkles, Map, Users } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";

const GlobeScene = lazy(() =>
  import("@/components/three/GlobeScene").then((m) => ({ default: m.GlobeScene })),
);

const features = [
  {
    icon: Sparkles,
    title: "AI-Powered Planning",
    description: "Let our AI generate complete day-by-day itineraries, suggest activities, and review your plans.",
  },
  {
    icon: Map,
    title: "Interactive Itinerary Builder",
    description: "Drag-and-drop stops, add activities, track budget, and manage packing lists in one place.",
  },
  {
    icon: Users,
    title: "Travel Community",
    description: "Share your adventures, discover other travelers' experiences, and get inspired.",
  },
];

export default function Landing() {
  return (
    <div className="flex flex-col">
      <section className="relative min-h-[90vh] flex items-center overflow-hidden">
        <div className="absolute inset-0 -z-10">
          <Suspense fallback={null}>
            <GlobeScene />
          </Suspense>
        </div>
        <div className="container relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="max-w-2xl"
          >
            <h1 className="text-5xl font-extrabold tracking-tight lg:text-6xl">
              Plan smarter trips with{" "}
              <span className="text-primary">AI</span>
            </h1>
            <p className="mt-4 text-lg text-muted-foreground">
              Traveloop combines intelligent itinerary planning, real-time data, and a vibrant
              traveler community to help you create unforgettable journeys.
            </p>
            <div className="flex gap-3 mt-8">
              <Link to="/register">
                <Button size="lg" className="gap-2">
                  Start for free <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link to="/cities">
                <Button size="lg" variant="outline">
                  Explore cities
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="py-20 bg-muted/30">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">Everything you need to travel well</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map(({ icon: Icon, title, description }) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="flex flex-col gap-3 p-6 rounded-xl border bg-background"
              >
                <Icon className="h-8 w-8 text-primary" />
                <h3 className="font-semibold text-lg">{title}</h3>
                <p className="text-sm text-muted-foreground">{description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 text-center">
        <div className="container max-w-xl">
          <h2 className="text-3xl font-bold mb-4">Ready to plan your next adventure?</h2>
          <p className="text-muted-foreground mb-8">
            Join thousands of travelers who use Traveloop to create their dream trips.
          </p>
          <Link to="/register">
            <Button size="lg">Create your free account</Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
