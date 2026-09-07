import { useState } from "react";

import {
  Link,
  useNavigate,
  useSearchParams,
} from "react-router-dom";

import AuthLayout from "../../components/auth/AuthLayout";
import AuthInput from "../../components/auth/AuthInput";

import useAuth from "../../hooks/useAuth";

import {
  validateEmail,
  validateName,
  validatePassword,
  validateConfirmPassword,
} from "../../utils/validation";

const Registration = () => {
  const navigate = useNavigate();

  const [searchParams] =
    useSearchParams();

  const { register } = useAuth();

  const role =
    searchParams.get("role");

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]:
        event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    /*
     * Validate role
     */

    if (
      role !== "exporter" &&
      role !== "provider"
    ) {
      setError(
        "Please select a valid account type."
      );

      return;
    }

    /*
     * Validate name
     */

    if (!validateName(form.name)) {
      setError(
        "Name must contain at least 2 characters."
      );

      return;
    }

    /*
     * Validate email
     */

    if (!validateEmail(form.email)) {
      setError(
        "Please enter a valid email address."
      );

      return;
    }

    /*
     * Backend requires minimum
     * 16 character password.
     */

    if (!validatePassword(form.password)) {
      setError(
        "Password must contain at least 16 characters."
      );

      return;
    }

    /*
     * Confirm password
     */

    if (
      !validateConfirmPassword(
        form.password,
        form.confirmPassword
      )
    ) {
      setError(
        "Passwords do not match."
      );

      return;
    }

    setLoading(true);

    try {
      await register({
        name: form.name,
        email: form.email,
        password: form.password,
        role: role,
        status: "active",
      });

      /*
       * Registration successful.
       * Send user to login.
       */

      navigate("/login", {
        replace: true,
        state: {
          registered: true,
        },
      });

    } catch (error) {
      setError(error.message);

    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>

      <div className="auth-form">

        <div className="auth-header">

          <span className="auth-eyebrow">
            CREATE ACCOUNT
          </span>

          <h2>
            Complete registration
          </h2>

          <p>
            Register as a{" "}
            <strong>
              {role === "provider"
                ? "Provider"
                : "Exporter"}
            </strong>
            .
          </p>

        </div>

        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>

          <AuthInput
            label="Full name"
            name="name"
            type="text"
            value={form.name}
            onChange={handleChange}
            placeholder="Enter your full name"
            autoComplete="name"
          />

          <AuthInput
            label="Email address"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            placeholder="you@example.com"
            autoComplete="email"
          />

          <AuthInput
            label="Password"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            placeholder="Minimum 16 characters"
            minLength={16}
            autoComplete="new-password"
          />

          <div className="password-hint">
            Your password must contain
            at least 16 characters.
          </div>

          <AuthInput
            label="Confirm password"
            name="confirmPassword"
            type="password"
            value={form.confirmPassword}
            onChange={handleChange}
            placeholder="Enter password again"
            minLength={16}
            autoComplete="new-password"
          />

          <button
            type="submit"
            className="auth-button"
            disabled={loading}
          >
            {loading
              ? "Creating account..."
              : "Create account"}
          </button>

        </form>

        <div className="auth-switch">

          <Link to="/signup">
            ← Change account type
          </Link>

        </div>

      </div>

    </AuthLayout>
  );
};

export default Registration;