import {
  createContext,
  useEffect,
  useState,
} from "react";

import {
  loginUser,
  registerUser,
  logoutUser,
} from "../services/authService";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  /*
   * Restore authentication state
   * when the application starts.
   */
  useEffect(() => {
    const storedToken =
      localStorage.getItem("access_token");

    const storedUser =
      localStorage.getItem("user");

    if (storedToken) {
      setToken(storedToken);
    }

    if (storedUser) {
      try {
        const parsed = JSON.parse(storedUser);
        if (!parsed.role) {
          parsed.role = parsed.email?.toLowerCase().includes("admin")
            ? "admin"
            : localStorage.getItem("provider_id")
            ? "provider"
            : "exporter";
        }
        setUser(parsed);
      } catch {
        localStorage.removeItem("user");
      }
    }

    setLoading(false);
  }, []);

  /*
   * LOGIN
   */
  const login = async (email, password) => {
    const data = await loginUser(
      email,
      password
    );

    const userData = {
      name: data.name,
      email: email,
      role: data.role || (email.toLowerCase().includes("admin") ? "admin" : "exporter"),
    };

    localStorage.setItem(
      "access_token",
      data.access_token
    );

    localStorage.setItem(
      "user",
      JSON.stringify(userData)
    );

    setToken(data.access_token);
    setUser(userData);

    return data;
  };

  /*
   * REGISTER
   */
  const register = async (userData) => {
    const data = await registerUser(userData);

    return data;
  };

  /*
   * LOGOUT
   */
  const logout = async () => {
    try {
      await logoutUser();
    } catch (error) {
      console.error(
        "Logout API error:",
        error
      );
    }

    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    setToken(null);
    setUser(null);
  };

  const isAuthenticated = Boolean(token);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        isAuthenticated,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};