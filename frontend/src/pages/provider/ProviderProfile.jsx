import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getProviderDetails } from "../../services/providerService";
import "../../assets/dashboard.css";

/*
|--------------------------------------------------------------------------
| ProviderProfile
|--------------------------------------------------------------------------
| Calls GET /providers/{provider_id}
| Reads the provider_id from localStorage (set after registration).
| Displays business details and approval status.
|--------------------------------------------------------------------------
*/

const getInitials = (name) =>
  name ? name[0].toUpperCase() : "P";

const ProviderProfile = () => {
  const [provider, setProvider] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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
        setProvider(data);
      } catch (err) {
        setError(err.message || "Failed to load provider profile.");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  /* ---- Loading ---- */
  if (loading) {
    return (
      <div className="loading-screen">Loading profile...</div>
    );
  }

  /* ---- Error / not registered ---- */
  if (error) {
    return (
      <div className="dashboard-page">
        <div className="page-header">
          <span className="page-eyebrow">MY ACCOUNT</span>
          <h1>Provider Profile</h1>
        </div>
        <div className="feedback-error">{error}</div>
        <Link to="/provider/register" className="btn btn-primary">
          Register as Provider
        </Link>
      </div>
    );
  }

  const statusClass =
    provider.approval_status?.toLowerCase() || "pending";

  return (
    <div className="dashboard-page">

      {/* Page header */}
      <div className="page-header">
        <span className="page-eyebrow">MY ACCOUNT</span>
        <h1>Provider Profile</h1>
        <p>Your business information registered on the platform.</p>
      </div>

      <div className="profile-card">

        {/* Card header */}
        <div className="profile-card-header">
          <div className="profile-avatar">
            {getInitials(provider.business_name)}
          </div>

          <div className="profile-card-title">
            <h2>{provider.business_name}</h2>
            <p>Logistics Provider · ID #{provider.provider_id}</p>
          </div>

          <span className={`status-badge ${statusClass}`}>
            {provider.approval_status || "Pending"}
          </span>
        </div>

        {/* Card body */}
        <div className="profile-card-body">
          <div className="info-grid">

            <div className="info-item">
              <label>Business Name</label>
              <p>{provider.business_name || "—"}</p>
            </div>

            <div className="info-item">
              <label>Contact</label>
              <p>{provider.contact || "—"}</p>
            </div>

            <div className="info-item info-full">
              <label>Business Address</label>
              <p>{provider.business_address || "—"}</p>
            </div>

            <div className="info-item">
              <label>Provider ID</label>
              <p>#{provider.provider_id}</p>
            </div>

            <div className="info-item">
              <label>Approval Status</label>
              <span className={`status-badge ${statusClass}`}>
                {provider.approval_status || "Pending"}
              </span>
            </div>

          </div>

          {/* Actions */}
          <div className="profile-actions">
            <Link to="/provider/edit" className="btn btn-primary">
              Edit Profile
            </Link>
            <Link to="/" className="btn btn-outline">
              Dashboard
            </Link>
          </div>
        </div>

      </div>
    </div>
  );
};

export default ProviderProfile;
