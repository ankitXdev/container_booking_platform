import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerProvider } from "../../services/providerService";
import "../../assets/dashboard.css";

/*
|--------------------------------------------------------------------------
| ProviderRegistration
|--------------------------------------------------------------------------
| Calls POST /providers/
| On success, saves provider_id to localStorage so that ProviderProfile
| and EditProviderProfile can look it up without needing it in the URL.
|--------------------------------------------------------------------------
*/

const ProviderRegistration = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    business_name: "",
    business_address: "",
    contact: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    if (error) setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.business_name.trim()) {
      setError("Business name is required (min 2 characters).");
      return;
    }

    if (!formData.business_address.trim() || formData.business_address.trim().length < 5) {
      setError("Business address is required (minimum 5 characters).");
      return;
    }

    if (!formData.contact.trim() || formData.contact.trim().length < 10) {
      setError("Contact is required (minimum 10 characters - phone or email).");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await registerProvider({
        business_name: formData.business_name.trim(),
        business_address: formData.business_address.trim(),
        contact: formData.contact.trim(),
      });

      /*
       * Store provider_id in localStorage so ProviderProfile
       * and EditProviderProfile pages can fetch the right record.
       */
      localStorage.setItem(
        "provider_id",
        data.provider_id
      );

      navigate("/provider/profile");
    } catch (err) {
      setError(err.message || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-page">

      {/* Page header */}
      <div className="page-header">
        <span className="page-eyebrow">SETUP</span>
        <h1>Register as Provider</h1>
        <p>
          Submit your business details. An admin will review and
          approve your account before you can list containers.
        </p>
      </div>

      <div className="edit-card">

        <div className="edit-card-header">
          <h2>Business Information</h2>
          <p>
            Fields marked{" "}
            <span style={{ color: "var(--autumn-ember)" }}>*</span>{" "}
            are required.
          </p>
        </div>

        <form onSubmit={handleSubmit}>

          <div className="edit-card-body">

            {error && (
              <div className="feedback-error">{error}</div>
            )}

            <div className="form-group">
              <label htmlFor="business_name">
                Business Name{" "}
                <span style={{ color: "var(--autumn-ember)" }}>
                  *
                </span>
              </label>
              <input
                id="business_name"
                name="business_name"
                type="text"
                value={formData.business_name}
                onChange={handleChange}
                placeholder="Your registered business name"
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="business_address">
                Business Address{" "}
                <span style={{ color: "var(--autumn-ember)" }}>*</span>
              </label>
              <input
                id="business_address"
                name="business_address"
                type="text"
                value={formData.business_address}
                onChange={handleChange}
                placeholder="Full address of your business (min 5 characters)"
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="contact">
                Contact Phone or Email{" "}
                <span style={{ color: "var(--autumn-ember)" }}>*</span>
              </label>
              <input
                id="contact"
                name="contact"
                type="text"
                value={formData.contact}
                onChange={handleChange}
                placeholder="Phone number or contact email (min 10 characters)"
                disabled={loading}
                required
              />
            </div>

          </div>

          <div className="edit-card-footer">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? "Submitting..." : "Submit for Approval"}
            </button>
          </div>

        </form>
      </div>
    </div>
  );
};

export default ProviderRegistration;