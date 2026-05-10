import { lazy, Suspense, useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, Sparkles, Map, Users, ChevronLeft, ChevronRight, MapPin, Star } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { heroImages } from "@/utils/cityImages";

const GlobeScene = lazy(() =>
  import("@/components/three/GlobeScene").then((m) => ({ default: m.GlobeScene })),
);

const features = [
  {
    icon: Sparkles,
    title: "AI-Powered Planning",
    description:
      "Generate complete day-by-day itineraries, get activity suggestions, and receive personalised trip feedback — all from a single prompt.",
    color: "text-violet-500",
    bg: "bg-violet-500/10",
  },
  {
    icon: Map,
    title: "Visual Itinerary Builder",
    description:
      "Drag-and-drop stops, attach activities, track your live budget, and manage packing lists — everything in one clean workspace.",
    color: "text-emerald-500",
    bg: "bg-emerald-500/10",
  },
  {
    icon: Users,
    title: "Travel Community",
    description:
      "Share stories, discover real traveller experiences, like posts, and get inspired by people who've been where you want to go.",
    color: "text-sky-500",
    bg: "bg-sky-500/10",
  },
];

const destinations = heroImages.slice(0, 6);

function HeroCarousel() {
  const [current, setCurrent] = useState(0);
  const [direction, setDirection] = useState(1);

  useEffect(() => {
    const id = setInterval(() => {
      setDirection(1);
      setCurrent((prev: number) => (prev + 1) % heroImages.length);
    }, 5000);
    return () => clearInterval(id);
  }, []);

  const go = (delta: number) => {
    setDirection(delta);
    setCurrent((prev: number) => (prev + delta + heroImages.length) % heroImages.length);
  };

  const img = heroImages[current];

  return (
    <div className="relative w-full h-full overflow-hidden">
      <AnimatePresence initial={false} custom={direction}>
        <motion.div
          key={current}
          custom={direction}
          variants={{
            enter: (d: number) => ({ x: d > 0 ? "100%" : "-100%", opacity: 0 }),
            center: { x: 0, opacity: 1 },
            exit: (d: number) => ({ x: d > 0 ? "-100%" : "100%", opacity: 0 }),
          }}
          initial="enter"
          animate="center"
          exit="exit"
          transition={{ duration: 0.7, ease: "easeInOut" }}
          className="absolute inset-0"
        >
          <img
            src={img.src}
            alt={img.city}
            className="h-full w-full object-cover"
            onError={(e) => { (e.currentTarget as HTMLImageElement).style.opacity = "0"; }}
          />
          <div className="absolute inset-0 bg-gradient-to-r from-black/60 via-black/30 to-transparent" />
        </motion.div>
      </AnimatePresence>

      {/* City label */}
      <motion.div
        key={`label-${current}`}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        className="absolute bottom-6 left-6 flex items-center gap-1.5 text-white/90 text-sm font-medium"
      >
        <MapPin className="h-3.5 w-3.5" />
        {img.city}, {img.country}
      </motion.div>

      {/* Controls */}
      <button
        type="button"
        aria-label="Previous destination"
        onClick={() => go(-1)}
        className="absolute left-3 top-1/2 -translate-y-1/2 h-9 w-9 rounded-full bg-black/30 hover:bg-black/50 flex items-center justify-center text-white transition-colors"
      >
        <ChevronLeft className="h-5 w-5" />
      </button>
      <button
        type="button"
        aria-label="Next destination"
        onClick={() => go(1)}
        className="absolute right-3 top-1/2 -translate-y-1/2 h-9 w-9 rounded-full bg-black/30 hover:bg-black/50 flex items-center justify-center text-white transition-colors"
      >
        <ChevronRight className="h-5 w-5" />
      </button>

      {/* Dots */}
      <div className="absolute bottom-6 right-6 flex gap-1.5">
        {heroImages.map((h, i) => (
          <button
            key={i}
            type="button"
            aria-label={`Go to ${h.city}`}
            onClick={() => { setDirection(i > current ? 1 : -1); setCurrent(i); }}
            className={`h-1.5 rounded-full transition-all ${
              i === current ? "w-6 bg-white" : "w-1.5 bg-white/40"
            }`}
          />
        ))}
      </div>
    </div>
  );
}

export default function Landing() {
  return (
    <div className="flex flex-col">
      {/* ── Hero ── */}
      <section className="relative min-h-[90vh] flex items-center overflow-hidden bg-neutral-950">
        {/* Background carousel */}
        <div className="absolute inset-0 -z-10">
          <HeroCarousel />
        </div>

        {/* Globe overlay (top-right, decorative) */}
        <div className="absolute right-0 top-0 bottom-0 w-1/2 hidden lg:block opacity-60 -z-10">
          <Suspense fallback={null}>
            <GlobeScene />
          </Suspense>
        </div>

        {/* Text content */}
        <div className="container relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="max-w-2xl text-white"
          >
            <span className="inline-flex items-center gap-2 text-sm font-medium bg-white/10 backdrop-blur px-3 py-1 rounded-full mb-5 border border-white/20">
              <Sparkles className="h-3.5 w-3.5 text-yellow-400" />
              AI-first travel planning
            </span>
            <h1 className="text-5xl font-extrabold tracking-tight lg:text-6xl leading-tight drop-shadow-lg">
              Plan smarter trips{" "}
              <br />
              <span className="text-primary">with AI</span>
            </h1>
            <p className="mt-5 text-lg text-white/80 leading-relaxed max-w-lg drop-shadow">
              Traveloop combines intelligent itinerary planning, curated destination data, and a
              vibrant traveller community to help you create unforgettable journeys.
            </p>
            <div className="flex flex-wrap gap-3 mt-8">
              <Link to="/register">
                <Button size="lg" className="gap-2 shadow-lg">
                  Start for free <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link to="/cities">
                <Button size="lg" variant="outline" className="bg-white/10 border-white/30 text-white hover:bg-white/20">
                  Explore destinations
                </Button>
              </Link>
            </div>
            <div className="flex gap-6 mt-8 text-white/70 text-sm">
              <span className="flex items-center gap-1"><Star className="h-3.5 w-3.5 fill-yellow-400 text-yellow-400" /> Free forever</span>
              <span>20+ curated destinations</span>
              <span>AI-generated itineraries</span>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── Destination grid ── */}
      <section className="py-20 bg-background">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold">Discover the world</h2>
            <p className="text-muted-foreground mt-2">
              20 hand-curated destinations with full itinerary data, cost breakdowns, and local tips.
            </p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {destinations.map(({ src, city, country }, i) => (
              <motion.div
                key={city}
                initial={{ opacity: 0, scale: 0.96 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.06 }}
              >
                <Link
                  to="/cities"
                  className={`group relative overflow-hidden rounded-xl block ${
                    i === 0 ? "md:col-span-2 md:row-span-2" : ""
                  }`}
                >
                  <div className={i === 0 ? "h-72 md:h-full" : "h-48"}>
                    <img
                      src={src}
                      alt={city}
                      className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-500"
                      onError={(e) => {
                        (e.currentTarget.parentElement as HTMLElement).style.background =
                          "hsl(var(--muted))";
                        e.currentTarget.style.display = "none";
                      }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                    <div className="absolute bottom-3 left-3 text-white">
                      <p className="font-semibold text-sm">{city}</p>
                      <p className="text-xs text-white/75">{country}</p>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
          <div className="text-center mt-6">
            <Link to="/cities">
              <Button variant="outline" className="gap-2">
                View all {heroImages.length} destinations <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold">Everything you need to travel well</h2>
            <p className="text-muted-foreground mt-2 max-w-xl mx-auto">
              From first idea to packed bag — Traveloop covers the whole journey.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {features.map(({ icon: Icon, title, description, color, bg }, i) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="flex flex-col gap-4 p-6 rounded-2xl border bg-background shadow-sm"
              >
                <div className={`h-12 w-12 rounded-xl ${bg} flex items-center justify-center`}>
                  <Icon className={`h-6 w-6 ${color}`} />
                </div>
                <h3 className="font-semibold text-lg">{title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="py-24 bg-primary text-primary-foreground">
        <div className="container max-w-2xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold mb-4">Ready for your next adventure?</h2>
            <p className="opacity-80 mb-8 max-w-lg mx-auto">
              Join travellers using Traveloop to plan smarter, travel better, and share their stories.
            </p>
            <div className="flex gap-3 justify-center flex-wrap">
              <Link to="/register">
                <Button size="lg" variant="secondary" className="gap-2 font-semibold">
                  Create your free account <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link to="/cities">
                <Button size="lg" variant="ghost" className="text-primary-foreground border border-primary-foreground/30 hover:bg-primary-foreground/10">
                  Browse destinations
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
