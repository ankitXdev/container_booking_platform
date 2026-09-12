import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import Login from "../pages/auth/Login";
import Signup from "../pages/auth/Signup";
import Registration from "../pages/auth/Registration";

import MainLayout from "../layouts/MainLayout";
import ProtectedRoute from "./ProtectedRoute";
import AdminRoute from "./AdminRoute";
import RoleRoute from "./RoleRoute";

// Provider pages
import ProviderRegistration from "../pages/provider/ProviderRegistration";
import ProviderProfile from "../pages/provider/ProviderProfile";
import EditProviderProfile from "../pages/provider/EditProviderProfile";
import SearchProviders from "../pages/provider/SearchProviders";
import ProviderDetail from "../pages/provider/ProviderDetail";

// Container pages
import ContainerSearch from "../pages/container/ContainerSearch";
import CreateContainer from "../pages/container/CreateContainer";
import ContainerDetail from "../pages/container/ContainerDetail";
import EditContainer from "../pages/container/EditContainer";

// Booking & Payment pages
import BookingList from "../pages/booking/BookingList";
import BookingDetail from "../pages/booking/BookingDetail";

// Dashboard page
import Dashboard from "../pages/dashboard/Dashboard";

// Admin page
import AdminDashboard from "../pages/admin/AdminDashboard";

// Compliance / Documents page
import DocumentVerification from "../pages/compliance/DocumentVerification";

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>

        {/* ======================
            PUBLIC AUTH ROUTES
        ====================== */}

        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/registration" element={<Registration />} />

        {/* ======================
            PROTECTED ROUTES
        ====================== */}

        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          {/* Role-based Dashboard landing */}
          <Route path="/" element={<Dashboard />} />

          {/* Container routes */}
          <Route path="/containers" element={<ContainerSearch />} />
          <Route
            path="/containers/create"
            element={
              <RoleRoute allowedRoles={["provider", "admin"]} redirectTo="/containers">
                <CreateContainer />
              </RoleRoute>
            }
          />
          <Route path="/containers/:id" element={<ContainerDetail />} />
          <Route
            path="/containers/:id/edit"
            element={
              <RoleRoute allowedRoles={["provider", "admin"]} redirectTo="/containers">
                <EditContainer />
              </RoleRoute>
            }
          />

          {/* Booking & Payment routes */}
          <Route path="/bookings" element={<BookingList />} />
          <Route path="/bookings/:id" element={<BookingDetail />} />

          {/* Provider-only management routes */}
          <Route
            path="/provider/register"
            element={
              <RoleRoute allowedRoles={["provider"]}>
                <ProviderRegistration />
              </RoleRoute>
            }
          />
          <Route
            path="/provider/profile"
            element={
              <RoleRoute allowedRoles={["provider"]}>
                <ProviderProfile />
              </RoleRoute>
            }
          />
          <Route
            path="/provider/edit"
            element={
              <RoleRoute allowedRoles={["provider"]}>
                <EditProviderProfile />
              </RoleRoute>
            }
          />

          {/* Provider Discovery & Public Details (Exporter / Admin) */}
          <Route
            path="/providers/search"
            element={
              <RoleRoute allowedRoles={["exporter", "admin"]} redirectTo="/containers">
                <SearchProviders />
              </RoleRoute>
            }
          />
          <Route
            path="/providers/:id"
            element={<ProviderDetail />}
          />

          {/* Compliance & Document routes */}
          <Route path="/documents" element={<DocumentVerification />} />

          {/* Admin routes */}
          <Route
            path="/admin"
            element={
              <AdminRoute>
                <AdminDashboard />
              </AdminRoute>
            }
          />
        </Route>

        {/* ======================
            UNKNOWN ROUTE
        ====================== */}

        <Route
          path="*"
          element={<Navigate to="/login" replace />}
        />

      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;