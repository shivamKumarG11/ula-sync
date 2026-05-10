import { Link, useNavigate } from "react-router-dom";
import { Globe, Menu, LogOut, User, Map, Users } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/hooks/useAuth";
import { useUIStore } from "@/store/uiStore";

export function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const { toggleSidebar } = useUIStore();
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center gap-4">
        {isAuthenticated && (
          <Button variant="ghost" size="icon" onClick={toggleSidebar} className="md:hidden">
            <Menu className="h-5 w-5" />
          </Button>
        )}

        <Link to="/" className="flex items-center gap-2 font-bold text-lg">
          <Globe className="h-5 w-5 text-primary" />
          Traveloop
        </Link>

        <nav className="hidden md:flex items-center gap-1 ml-4">
          <Link to="/cities">
            <Button variant="ghost" size="sm" className="gap-2">
              <Map className="h-4 w-4" />
              Explore
            </Button>
          </Link>
          <Link to="/community">
            <Button variant="ghost" size="sm" className="gap-2">
              <Users className="h-4 w-4" />
              Community
            </Button>
          </Link>
        </nav>

        <div className="ml-auto flex items-center gap-2">
          {isAuthenticated && user ? (
            <>
              <Link to={`/u/${user.username}/dashboard`}>
                <Button variant="ghost" size="sm" className="gap-2">
                  <User className="h-4 w-4" />
                  {user.username}
                </Button>
              </Link>
              <Button variant="ghost" size="icon" onClick={() => { logout(); navigate("/"); }}>
                <LogOut className="h-4 w-4" />
              </Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variant="ghost" size="sm">Sign in</Button>
              </Link>
              <Link to="/register">
                <Button size="sm">Get started</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
