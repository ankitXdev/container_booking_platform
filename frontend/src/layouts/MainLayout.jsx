import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import "../assets/dashboard.css";

/*
|--------------------------------------------------------------------------
| MainLayout
|--------------------------------------------------------------------------
| Wraps all authenticated pages with a top navigation bar.
| Nav links use NavLink for active-state highlighting.
|--------------------------------------------------------------------------
*/

const MainLayout = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="main-layout">

      <header className="main-header">

        {/* Logo */}
        <Link to="/" className="main-logo">
          CB
        </Link>

        {/* Navigation links */}
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

          <NavLink
            to="/providers/search"
            className={({ isActive }) =>
              "nav-link" + (isActive ? " active" : "")
            }
          >
            Search Providers
          </NavLink>

          <NavLink
            to="/provider/profile"
            className={({ isActive }) =>
              "nav-link" + (isActive ? " active" : "")
            }
          >
            My Profile
          </NavLink>
        </nav>

        {/* User info + logout */}
        <div className="nav-right">
          <span className="user-name">{user?.name}</span>
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