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

const Dashboard = () => {
  return (
    <div>
      <h1>Dashboard</h1>

      <p>
        Authentication successful.
      </p>
    </div>
  );
};

const AppRoutes = () => {
  return (
    <BrowserRouter>

      <Routes>

        {/* ======================
            PUBLIC AUTH ROUTES
        ====================== */}

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/signup"
          element={<Signup />}
        />

        <Route
          path="/registration"
          element={<Registration />}
        />

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

          <Route
            path="/"
            element={<Dashboard />}
          />

        </Route>

        {/* ======================
            UNKNOWN ROUTE
        ====================== */}

        <Route
          path="*"
          element={
            <Navigate
              to="/login"
              replace
            />
          }
        />

      </Routes>

    </BrowserRouter>
  );
};

export default AppRoutes;