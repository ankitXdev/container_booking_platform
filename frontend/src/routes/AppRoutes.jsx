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

import ProviderRegistration from "../pages/provider/ProviderRegistration";
import ProviderProfile from "../pages/provider/ProviderProfile";
import EditProviderProfile from "../pages/provider/EditProviderProfile";
import SearchProviders from "../pages/provider/SearchProviders";

/*
|--------------------------------------------------------------------------
| Placeholder dashboard — will be replaced in a future phase.
|--------------------------------------------------------------------------
*/
const Dashboard = () => (
  <div>
    <h1>Dashboard</h1>
    <p>Authentication successful.</p>
  </div>
);

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
          {/* Dashboard */}
          <Route path="/" element={<Dashboard />} />

          {/* Provider routes */}
          <Route
            path="/provider/register"
            element={<ProviderRegistration />}
          />
          <Route
            path="/provider/profile"
            element={<ProviderProfile />}
          />
          <Route
            path="/provider/edit"
            element={<EditProviderProfile />}
          />
          <Route
            path="/providers/search"
            element={<SearchProviders />}
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