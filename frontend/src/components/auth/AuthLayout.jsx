import { Link } from "react-router-dom";

const AuthLayout = ({ children }) => {
  return (
    <div className="auth-page">

      <div className="auth-container">

        {/* LEFT SIDE */}

        <div className="auth-brand">

          <Link
            to="/login"
            className="auth-logo"
          >
            CB
          </Link>

          <div className="brand-content">

            <span className="brand-label">
              CONTAINER BOOKING
            </span>

            <h1>
              Move your containers
              with confidence.
            </h1>

            <p>
              Connect exporters with
              reliable container service
              providers through one
              simple platform.
            </p>

            <div className="brand-features">

              <div className="feature">
                <span>✓</span>
                <p>Verified service providers</p>
              </div>

              <div className="feature">
                <span>✓</span>
                <p>Simple container management</p>
              </div>

              <div className="feature">
                <span>✓</span>
                <p>Secure account access</p>
              </div>

            </div>

          </div>

        </div>

        {/* RIGHT SIDE */}

        <div className="auth-content">
          {children}
        </div>

      </div>

    </div>
  );
};

export default AuthLayout;