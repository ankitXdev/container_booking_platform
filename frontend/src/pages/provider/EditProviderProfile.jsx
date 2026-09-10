import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  getProviderDetails,
  updateProvider,
} from "../../services/providerService";
import "../../assets/dashboard.css";

/*
|--------------------------------------------------------------------------
| EditProviderProfile
|--------------------------------------------------------------------------
| On mount: fetches GET /providers/{id} and pre-fills the form.
| On submit: calls PUT /providers/{id} then redirects to /provider/profile.
|--------------------------------------------------------------------------
*/

const EditProviderProfile = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    business_name: "",
    business_address: "",
    contact: "",
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  /* ---- Pre-fill form on mount ---- */
  useEffect(() => {
    const fetchProfile = async () => {
      const providerId = localStorage.getItem("provider_id");

      if (!providerId) {
        setError(
          "No provider profile found. Please complete provider registration first."
        );
        setLoading(false);
        return;
      }

      try {
        const data = await getProviderDetails(providerId);

        setForm({
          business_name: data.business_name || "",
          business_address: data.business_address || "",
          contact: data.contact || "",
        });
      } catch (err) {
        setError(err.message || "Failed to load profile.");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (error) setError("");
    if (success) setSuccess("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.business_name.trim()) {
      setError("Business name is required.");
      return;
    }

    const providerId = localStorage.getItem("provider_id");

    if (!providerId) {
      setError("Provider ID not found. Please re-register.");
      return;
    }

    setSaving(true);
    setError("");

    try {
      await updateProvider(providerId, form);
      setSuccess("Profile updated successfully. Redirecting...");
      setTimeout(() => navigate("/provider/profile"), 1200);
    } catch (err) {
      setError(err.message || "Failed to update profile.");
    } finally {
      setSaving(false);
    }
  };

  /* ---- Loading ---- */
  if (loading) {
    return (
      <div className="loading-screen">Loading profile...</div>
    );
  }

  return (
    <div className="dashboard-page">

      {/* Page header */}
      <div className="page-header">
        <span className="page-eyebrow">MY ACCOUNT</span>
        <h1>Edit Profile</h1>
        <p>Update your business information shown to exporters.</p>
      </div>

      <div className="edit-card">

        <div className="edit-card-header">
          <h2>Business Information</h2>
          <p>Changes will be saved to your provider profile.</p>
        </div>

        <form onSubmit={handleSubmit}>

          <div className="edit-card-body">

            {error && (
              <div className="feedback-error">{error}</div>
            )}

            {success && (
              <div className="feedback-success">{success}</div>
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
                value={form.business_name}
                onChange={handleChange}
                placeholder="Your registered business name"
                disabled={saving}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="business_address">
                Business Address
              </label>
              <input
                id="business_address"
                name="business_address"
                type="text"
                value={form.business_address}
                onChange={handleChange}
                placeholder="Full address of your business"
                disabled={saving}
              />
            </div>

            <div className="form-group">
              <label htmlFor="contact">Contact</label>
              <input
                id="contact"
                name="contact"
                type="text"
                value={form.contact}
                onChange={handleChange}
                placeholder="Phone number or business email"
                disabled={saving}
              />
            </div>

          </div>

          <div className="edit-card-footer">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={saving}
            >
              {saving ? "Saving..." : "Save Changes"}
            </button>

            <Link
              to="/provider/profile"
              className="btn btn-outline"
            >
              Cancel
            </Link>
          </div>

        </form>
      </div>
    </div>
  );
};

export default EditProviderProfile;
