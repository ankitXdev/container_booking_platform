import { Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

/*
|--------------------------------------------------------------------------
| AdminRoute
|--------------------------------------------------------------------------
| Protects routes that require platform administrator privileges.
| Non-admin users are safely redirected away from administrative consoles.
|--------------------------------------------------------------------------
*/

const AdminRoute = ({ children }) => {
  const { user, token, loading } = useAuth();

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="empty-state">
          <h3>Checking permissions...</h3>
        </div>
      </div>
    );
  }

  // Not logged in
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Logged in but not an admin
  if (user?.role !== "admin") {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default AdminRoute;
