import { useState } from "react";
import {
  Link,
  useNavigate,
} from "react-router-dom";

import AuthLayout from "../../components/auth/AuthLayout";
import AuthInput from "../../components/auth/AuthInput";

import useAuth from "../../hooks/useAuth";

import {
  validateEmail,
} from "../../utils/validation";

const Login = () => {
  const navigate = useNavigate();

  const { login } = useAuth();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");

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

    if (!validateEmail(form.email)) {
      setError(
        "Please enter a valid email address."
      );

      return;
    }

    if (!form.password) {
      setError(
        "Please enter your password."
      );

      return;
    }

    setLoading(true);

    try {
      await login(
        form.email,
        form.password
      );

      navigate("/", {
        replace: true,
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
            WELCOME BACK
          </span>

          <h2>
            Sign in to your account
          </h2>

          <p>
            Enter your credentials to
            continue.
          </p>

        </div>

        {error && (
          <div className="auth-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>

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
            placeholder="Enter your password"
            autoComplete="current-password"
          />

          <button
            type="submit"
            className="auth-button"
            disabled={loading}
          >
            {loading
              ? "Signing in..."
              : "Sign in"}
          </button>

        </form>

        <div className="auth-switch">

          <span>
            Don't have an account?
          </span>

          <Link to="/signup">
            Create account
          </Link>

        </div>

      </div>

    </AuthLayout>
  );
};

export default Login;
