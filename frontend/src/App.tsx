import { lazy, Suspense } from "react";
import {
  createBrowserRouter,
  RouterProvider,
  Outlet,
  Navigate,
} from "react-router-dom";
import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import { AuthGuard } from "@/components/layout/AuthGuard";
import { AdminGuard } from "@/components/layout/AdminGuard";
import { Spinner } from "@/components/ui/Spinner";
import { AIChatbot } from "@/components/ai/AIChatbot";

const Landing = lazy(() => import("@/pages/Landing"));
const Auth = lazy(() => import("@/pages/Auth"));
const Onboarding = lazy(() => import("@/pages/Onboarding"));
const Dashboard = lazy(() => import("@/pages/Dashboard"));
const MyTrips = lazy(() => import("@/pages/MyTrips"));
const CreateTrip = lazy(() => import("@/pages/CreateTrip"));
const ItineraryBuilder = lazy(() => import("@/pages/ItineraryBuilder"));
const ItineraryView = lazy(() => import("@/pages/ItineraryView"));
const PackingChecklist = lazy(() => import("@/pages/PackingChecklist"));
const TripInfo = lazy(() => import("@/pages/TripInfo"));
const CitySearch = lazy(() => import("@/pages/CitySearch"));
const Community = lazy(() => import("@/pages/Community"));
const Profile = lazy(() => import("@/pages/Profile"));
const Admin = lazy(() => import("@/pages/Admin"));
const AdminUsers = lazy(() => import("@/pages/AdminUsers"));
const AdminCities = lazy(() => import("@/pages/AdminCities"));
const AdminAnalytics = lazy(() => import("@/pages/AdminAnalytics"));
const NotFound = lazy(() => import("@/pages/NotFound"));

function PageFallback() {
  return (
    <div className="flex h-48 items-center justify-center">
      <Spinner />
    </div>
  );
}

function PublicLayout() {
  return (
    <>
      <Navbar />
      <Suspense fallback={<PageFallback />}>
        <Outlet />
      </Suspense>
    </>
  );
}

function AppLayout() {
  return (
    <>
      <Navbar />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 min-h-screen">
          <Suspense fallback={<PageFallback />}>
            <Outlet />
          </Suspense>
        </main>
      </div>
      <AIChatbot />
    </>
  );
}

function AdminLayout() {
  return (
    <AdminGuard>
      <AppLayout />
    </AdminGuard>
  );
}

const router = createBrowserRouter([
  {
    element: <PublicLayout />,
    children: [
      { path: "/", element: <Landing /> },
      { path: "/login", element: <Auth /> },
      { path: "/register", element: <Auth /> },
      { path: "/trips/:tripId/view", element: <ItineraryView /> },
    ],
  },
  {
    element: (
      <AuthGuard>
        <AppLayout />
      </AuthGuard>
    ),
    children: [
      { path: "/onboarding", element: <Onboarding /> },
      { path: "/dashboard", element: <Dashboard /> },
      { path: "/trips", element: <MyTrips /> },
      { path: "/trips/new", element: <CreateTrip /> },
      { path: "/trips/:tripId/build", element: <ItineraryBuilder /> },
      { path: "/trips/:tripId/packing", element: <PackingChecklist /> },
      { path: "/trips/:tripId/info", element: <TripInfo /> },
      { path: "/cities", element: <CitySearch /> },
      { path: "/community", element: <Community /> },
      { path: "/profile", element: <Profile /> },
    ],
  },
  {
    element: <AdminLayout />,
    children: [
      {
        path: "/admin",
        element: <Admin />,
        children: [
          { index: true, element: <Navigate to="/admin/users" replace /> },
          { path: "users", element: <AdminUsers /> },
          { path: "cities", element: <AdminCities /> },
          { path: "analytics", element: <AdminAnalytics /> },
        ],
      },
    ],
  },
  {
    path: "*",
    element: (
      <Suspense fallback={<PageFallback />}>
        <NotFound />
      </Suspense>
    ),
  },
]);

export default function App() {
  return <RouterProvider router={router} />;
}
