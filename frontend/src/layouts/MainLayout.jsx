import {
  Link,
  Outlet,
  useNavigate,
} from "react-router-dom";

import useAuth from "../hooks/useAuth";

const MainLayout = () => {
  const navigate = useNavigate();

  const {
    user,
    logout,
  } = useAuth();

  const handleLogout = async () => {
    await logout();

    navigate("/login", {
      replace: true,
    });
  };

  return (
    <div className="main-layout">

      <header className="main-header">

        <Link
          to="/"
          className="main-logo"
        >
          CB
        </Link>

        <nav>

          <span className="user-name">
            {user?.name}
          </span>

          <button
            onClick={handleLogout}
            className="logout-button"
          >
            Logout
          </button>

        </nav>

      </header>

      <main className="main-content">
        <Outlet />
      </main>

    </div>
  );
};

export default MainLayout;