import { useState } from "react";

import {
  Link,
  useNavigate,
} from "react-router-dom";

import AuthLayout from "../../components/auth/AuthLayout";

import RoleSelector from "../../components/auth/RoleSelector";

const Signup = () => {
  const navigate = useNavigate();

  const [role, setRole] =
    useState("");

  const handleContinue = () => {
    if (!role) {
      return;
    }

    navigate(
      `/registration?role=${role}`
    );
  };

  return (
    <AuthLayout>

      <div className="auth-form">

        <div className="auth-header">

          <span className="auth-eyebrow">
            GET STARTED
          </span>

          <h2>
            Create an account
          </h2>

          <p>
            Choose how you want to use
            the platform.
          </p>

        </div>

        <RoleSelector
          role={role}
          setRole={setRole}
        />

        <button
          type="button"
          className="auth-button"
          disabled={!role}
          onClick={handleContinue}
        >
          Continue
        </button>

        <div className="auth-switch">

          <span>
            Already have an account?
          </span>

          <Link to="/login">
            Sign in
          </Link>

        </div>

      </div>

    </AuthLayout>
  );
};

export default Signup;