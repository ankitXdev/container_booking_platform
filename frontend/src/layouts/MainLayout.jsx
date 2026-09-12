import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import "../assets/dashboard.css";

/*
|--------------------------------------------------------------------------
| MainLayout
|--------------------------------------------------------------------------
| Wraps all authenticated pages with a top navigation bar.
| Navigation links are dynamically tailored based on the user's role:
| - Exporters see: Dashboard, Browse Space, My Shipments, Find Providers
| - Providers see: Dashboard, My Fleet, + Add Container, Customer Bookings, Company Profile
| - Admins see: Dashboard, Admin Console, All Containers, All Bookings
|--------------------------------------------------------------------------
*/

const MainLayout = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const role = user?.role?.toLowerCase() || "exporter";

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="main-layout">

      <header className="main-header">

        {/* Logo */}
        <Link to="/" className="main-logo" title="Cargo Booking Platform">
          CB
        </Link>

        {/* Navigation links - Role-Differentiated */}
        <nav className="nav-links">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              "nav-link" + (isActive ? " active" : "")
            }
          >
            Dashboard
          </NavLink>

          {/* EXPORTER NAVIGATION */}
          {role === "exporter" && (
            <>
              <NavLink
                to="/containers"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                Browse Space
              </NavLink>

              <NavLink
                to="/bookings"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                My Shipments
              </NavLink>

              <NavLink
                to="/providers/search"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                Find Providers
              </NavLink>

              <NavLink
                to="/documents"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                KYC & Docs
              </NavLink>
            </>
          )}

          {/* PROVIDER NAVIGATION */}
          {role === "provider" && (
            <>
              <NavLink
                to="/containers"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                My Fleet
              </NavLink>

              <NavLink
                to="/containers/create"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                + Add Container
              </NavLink>

              <NavLink
                to="/bookings"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                Customer Bookings
              </NavLink>

              <NavLink
                to="/provider/profile"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                Company Profile
              </NavLink>

              <NavLink
                to="/documents"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                Licenses & Docs
              </NavLink>
            </>
          )}

          {/* ADMIN NAVIGATION */}
          {role === "admin" && (
            <>
              <NavLink
                to="/admin"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                Admin Console
              </NavLink>

              <NavLink
                to="/containers"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                All Containers
              </NavLink>

              <NavLink
                to="/bookings"
                className={({ isActive }) =>
                  "nav-link" + (isActive ? " active" : "")
                }
              >
                All Bookings
              </NavLink>
            </>
          )}
        </nav>

        {/* User info + role badge + logout */}
        <div className="nav-right" style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ textAlign: "right" }}>
            <span className="user-name" style={{ display: "block", lineHeight: 1.2 }}>
              {user?.name || "Account"}
            </span>
            <span
              style={{
                fontSize: 10,
                fontWeight: 800,
                letterSpacing: "0.5px",
                textTransform: "uppercase",
                padding: "2px 6px",
                borderRadius: 4,
                background:
                  role === "admin"
                    ? "#DC2626"
                    : role === "provider"
                    ? "#2563EB"
                    : "#D97706",
                color: "#FFFFFF",
              }}
            >
              {role}
            </span>
          </div>

          <button
            onClick={handleLogout}
            className="logout-button"
          >
            Logout
          </button>
        </div>

      </header>

      <main className="main-content">
        <Outlet />
      </main>

    </div>
  );
};

export default MainLayout;