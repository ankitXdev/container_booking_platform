import { Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

/*
|--------------------------------------------------------------------------
| RoleRoute
|--------------------------------------------------------------------------
| Enforces role-based route access. If the user's role is not included in
| allowedRoles, they are safely redirected away (e.g. to Dashboard /).
|--------------------------------------------------------------------------
*/

const RoleRoute = ({ children, allowedRoles = [], redirectTo = "/" }) => {
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

  const role = user?.role?.toLowerCase();

  // If role is not allowed, redirect
  if (!role || (allowedRoles.length > 0 && !allowedRoles.includes(role))) {
    return <Navigate to={redirectTo} replace />;
  }

  return children;
};

export default RoleRoute;
