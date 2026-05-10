import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Home, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <motion.div
        className="flex flex-col items-center gap-6 text-center px-4"
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="relative">
          <p className="text-[120px] font-black leading-none text-muted-foreground/20 select-none">
            404
          </p>
          <p className="absolute inset-0 flex items-center justify-center text-4xl">🗺️</p>
        </div>
        <div>
          <h1 className="text-2xl font-bold">Page not found</h1>
          <p className="text-muted-foreground mt-1 max-w-sm">
            Looks like this destination doesn't exist on our map yet.
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline" asChild>
            <Link to={-1 as unknown as string}>
              <ArrowLeft className="h-4 w-4 mr-1" />
              Go Back
            </Link>
          </Button>
          <Button asChild>
            <Link to="/">
              <Home className="h-4 w-4 mr-1" />
              Home
            </Link>
          </Button>
        </div>
      </motion.div>
    </div>
  );
}
