import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import {
  getContainerDetails,
  updateContainerAvailability,
  deleteContainer,
} from "../../services/containerService";
import { createBooking } from "../../services/bookingService";
import { getExporterComplianceStatus } from "../../services/documentService";
import useAuth from "../../hooks/useAuth";
import "../../assets/dashboard.css";

const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleString("en-IN", {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const ContainerDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const role = user?.role?.toLowerCase() || "exporter";
  const myProviderId = localStorage.getItem("provider_id");
  const isContainerOwner =
    role === "admin" ||
    (role === "provider" && myProviderId && container && String(container.provider_id) === String(myProviderId));

  // Core container state
  const [container, setContainer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionSuccess, setActionSuccess] = useState("");

  // Booking space state
  const [bookingCapacity, setBookingCapacity] = useState("");
  const [bookingLoading, setBookingLoading] = useState(false);
  const [bookingError, setBookingError] = useState("");

  // Compliance state for Exporter
  const [complianceStatus, setComplianceStatus] = useState(null);

  // Delete modal state
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  // Fetch container details
  const fetchDetails = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getContainerDetails(id);
      setContainer(data);
      if (role === "exporter") {
        try {
          const comp = await getExporterComplianceStatus();
          setComplianceStatus(comp);
        } catch {
          // ignore
        }
      }
    } catch (err) {
      setError(err.message || "Failed to load container details.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetails();
  }, [id]);

  // Toggle container availability
  const handleToggleAvailability = async () => {
    if (!container) return;
    setActionSuccess("");
    setError("");
    try {
      const newStatus = !container.is_available;
      await updateContainerAvailability(id, newStatus);
      setContainer((prev) => ({ ...prev, is_available: newStatus }));
      setActionSuccess(
        `Container #${id} is now marked as ${newStatus ? "Available" : "Unavailable"}.`
      );
    } catch (err) {
      setError(err.message || "Failed to update availability.");
    }
  };

  // Delete container listing
  const handleDelete = async () => {
    setDeleteLoading(true);
    setError("");
    try {
      await deleteContainer(id);
      navigate("/containers");
    } catch (err) {
      setError(err.message || "Failed to delete container.");
      setShowDeleteModal(false);
    } finally {
      setDeleteLoading(false);
    }
  };

  // Handle cargo space reservation
  const handleBookSpace = async (e) => {
    e.preventDefault();
    setBookingError("");

    const requestedKg = parseFloat(bookingCapacity);
    if (isNaN(requestedKg) || requestedKg <= 0) {
      setBookingError("Please enter a valid weight in kilograms.");
      return;
    }

    if (requestedKg > container.available_capacity_kg) {
      setBookingError(
        `Requested capacity (${requestedKg} kg) exceeds available capacity (${container.available_capacity_kg} kg).`
      );
      return;
    }

    setBookingLoading(true);
    try {
      const newBooking = await createBooking({
        container_id: container.container_id,
        booked_capacity_kg: requestedKg,
      });

      // Redirect immediately to the new booking for payment / tracking
      navigate(`/bookings/${newBooking.booking_id}`);
    } catch (err) {
      setBookingError(err.message || "Failed to reserve container space.");
    } finally {
      setBookingLoading(false);
    }
  };

  // Quick preset button helper
  const handleQuickAdd = (amount) => {
    if (!container) return;
    const current = parseFloat(bookingCapacity) || 0;
    const nextVal = Math.min(current + amount, container.available_capacity_kg);
    setBookingCapacity(String(nextVal));
    if (bookingError) setBookingError("");
  };

  const handleSetMax = () => {
    if (!container) return;
    setBookingCapacity(String(container.available_capacity_kg));
    if (bookingError) setBookingError("");
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="empty-state">
          <h3>Loading container details...</h3>
          <p>Connecting to platform cargo schedule...</p>
        </div>
      </div>
    );
  }

  if (error && !container) {
    return (
      <div className="dashboard-page">
        <div className="feedback-error">{error}</div>
        <Link to="/containers" className="btn btn-outline" style={{ marginTop: 16 }}>
          ← Back to Containers
        </Link>
      </div>
    );
  }

  // Capacity calculation
  const bookedKg = container.total_capacity_kg - container.available_capacity_kg;
  const bookedPercent = Math.min(
    100,
    Math.max(0, Math.round((bookedKg / container.total_capacity_kg) * 100))
  );
  const availablePercent = 100 - bookedPercent;

  const estimatedTotal =
    bookingCapacity && !isNaN(parseFloat(bookingCapacity))
      ? (parseFloat(bookingCapacity) * container.price_per_kg).toFixed(2)
      : null;

  return (
    <div className="dashboard-page">
      {/* Top breadcrumb navigation */}
      <div style={{ marginBottom: 16, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <Link to="/containers" className="btn btn-outline btn-sm">
          ← Back to All Containers
        </Link>
        <span style={{ fontSize: 12, color: "var(--text-muted)", fontWeight: 600 }}>
          Container Listing #{container.container_id}
        </span>
      </div>

      {actionSuccess && <div className="feedback-success">{actionSuccess}</div>}
      {error && <div className="feedback-error">{error}</div>}

      <div className="container-detail-card" style={{ maxWidth: 900 }}>
        {/* Header with Route Banner */}
        <div className="container-detail-header">
          <div className="route-detail-wrap" style={{ marginBottom: 14 }}>
            <div className="route-detail-port">
              <span className="route-detail-port-icon">🏭</span>
              <span className="route-detail-city">{container.origin}</span>
              <span className="route-detail-sub">Origin Port</span>
            </div>
            <div className="route-detail-mid">
              <span className="route-detail-ship">🚢</span>
              <div className="route-detail-line" />
            </div>
            <div className="route-detail-port">
              <span className="route-detail-port-icon">⚓</span>
              <span className="route-detail-city">{container.destination}</span>
              <span className="route-detail-sub">Destination Port</span>
            </div>
          </div>
          <div className="container-detail-meta">
            <span
              className={`availability-badge ${
                container.is_available ? "available" : "unavailable"
              }`}
            >
              {container.is_available ? "✓ Available for Booking" : "✕ Unavailable / Full"}
            </span>
            <span className="container-detail-date">
              📅 Departure: {formatDate(container.departure_date)}
            </span>
          </div>
        </div>

        {/* Body */}
        <div className="container-detail-body">
          {/* Key Metrics Grid */}
          <div className="profile-grid" style={{ marginBottom: 24 }}>
            <div className="profile-field">
              <label>AVAILABLE SPACE</label>
              <p style={{ fontSize: 22, color: "var(--autumn-ember)", fontWeight: 800 }}>
                {container.available_capacity_kg.toLocaleString()} kg
              </p>
              <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
                {availablePercent}% of total capacity open
              </span>
            </div>

            <div className="profile-field">
              <label>TOTAL VESSEL CAPACITY</label>
              <p style={{ fontSize: 20, fontWeight: 700 }}>
                {container.total_capacity_kg.toLocaleString()} kg
              </p>
              <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
                {bookedKg.toLocaleString()} kg already reserved
              </span>
            </div>

            <div className="profile-field">
              <label>CARGO FREIGHT RATE</label>
              <p style={{ fontSize: 22, fontWeight: 800, color: "var(--coffee-bean)" }}>
                ₹{container.price_per_kg.toFixed(2)}
                <span style={{ fontSize: 13, fontWeight: 500, color: "var(--text-secondary)" }}> / kg</span>
              </p>
              <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
                Standard commercial cargo tariff
              </span>
            </div>

            <div className="profile-field">
              <label>LISTING ID</label>
              <p style={{ fontSize: 18, fontWeight: 600 }}>
                #{container.container_id}
              </p>
              <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
                ISO Shipping Container
              </span>
            </div>
          </div>

          {/* Visual Capacity Utilization Bar */}
          <div
            style={{
              background: "var(--surface)",
              borderRadius: 12,
              padding: "16px 20px",
              marginBottom: 24,
              border: "1px solid var(--border)",
            }}
          >
            <div className="cap-bar-wrap">
              <div className="cap-bar-header">
                <span>Capacity Utilization</span>
                <span className={`cap-bar-pct ${availablePercent > 50 ? "green" : availablePercent >= 20 ? "amber" : "red"}`}>
                  {availablePercent}% free — {container.available_capacity_kg.toLocaleString()} kg of {container.total_capacity_kg.toLocaleString()} kg
                </span>
              </div>
              <div className="cap-bar-track">
                <div
                  className="cap-bar-filled"
                  style={{ width: `${bookedPercent}%` }}
                  title={`Booked: ${bookedKg.toLocaleString()} kg`}
                />
                <div
                  className={`cap-bar-free ${availablePercent > 50 ? "green" : availablePercent >= 20 ? "amber" : "red"}`}
                  style={{ width: `${availablePercent}%` }}
                  title={`Available: ${container.available_capacity_kg.toLocaleString()} kg`}
                />
              </div>
              <div className="cap-bar-legend">
                <span>
                  <span className={`cap-bar-dot ${availablePercent > 50 ? "green" : availablePercent >= 20 ? "amber" : "red"}`} />
                  {container.available_capacity_kg.toLocaleString()} kg available
                </span>
                <span>
                  <span className="cap-bar-dot grey" />
                  {bookedKg.toLocaleString()} kg occupied / reserved
                </span>
              </div>
            </div>
          </div>

          {/* Provider Card Section */}
          <div
            style={{
              background: "var(--surface)",
              borderRadius: 12,
              padding: "18px 22px",
              marginBottom: 24,
              border: "1px solid var(--border)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: 14,
            }}
          >
            <div>
              <span
                style={{
                  fontSize: 10,
                  fontWeight: 800,
                  color: "#059669",
                  letterSpacing: "0.5px",
                  textTransform: "uppercase",
                  background: "#D1FAE5",
                  padding: "2px 8px",
                  borderRadius: 4,
                  display: "inline-block",
                  marginBottom: 6,
                }}
              >
                ✓ Verified Logistics Partner
              </span>
              <h3 style={{ margin: "2px 0 6px", color: "var(--coffee-bean)", fontSize: 18 }}>
                {container.provider_business_name || "Ocean Logistics Partner"}
              </h3>
              <p style={{ margin: 0, fontSize: 13, color: "var(--text-secondary)" }}>
                Contact Details: <strong>{container.provider_contact || "N/A"}</strong>
              </p>
            </div>

            <Link
              to={`/providers/${container.provider_id}`}
              className="btn btn-outline btn-sm"
            >
              View Provider Profile & Fleet →
            </Link>
          </div>

          {/* =========================================================
              EXPORTER BOOKING SECTION
          ========================================================= */}
          {role === "exporter" && (
            <>
              {container.is_available && container.available_capacity_kg > 0 ? (
                <div
                  style={{
                    border: "2px solid rgba(183, 79, 13, 0.3)",
                    borderRadius: 12,
                    padding: "24px",
                    background: "#FFFBF7",
                    marginBottom: 24,
                  }}
                >
                  <h3 style={{ margin: "0 0 6px", fontSize: 18, color: "var(--coffee-bean)" }}>
                    Book Container Space
                  </h3>
                  <p style={{ margin: "0 0 16px", fontSize: 13, color: "var(--text-secondary)" }}>
                    Select how many kilograms of cargo you want to ship on this voyage.
                  </p>

                  {/* Verification Banner if not verified */}
                  {complianceStatus && !complianceStatus.is_verified && (
                    <div
                      style={{
                        background: "#FFFBEB",
                        border: "1px solid #FCD34D",
                        borderRadius: 8,
                        padding: "12px 16px",
                        marginBottom: 16,
                      }}
                    >
                      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                        <span style={{ fontSize: 18 }}>⚠️</span>
                        <strong style={{ fontSize: 13, color: "#92400E" }}>
                          Account Verification Required
                        </strong>
                      </div>
                      <p style={{ margin: "0 0 8px", fontSize: 12, color: "#78350F" }}>
                        {complianceStatus.status === "PENDING"
                          ? "Your business documents are pending admin review. You will be able to book container space once approved."
                          : "Please upload your business registration / IEC documents to unlock container bookings."}
                      </p>
                      <Link to="/documents" className="btn btn-outline btn-sm" style={{ padding: "4px 10px", fontSize: 12 }}>
                        Go to Document Verification →
                      </Link>
                    </div>
                  )}

                  {bookingError && <div className="feedback-error">{bookingError}</div>}

                  <form onSubmit={handleBookSpace}>
                    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                      <div>
                        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                          <label
                            style={{
                              fontSize: 12,
                              fontWeight: 700,
                              color: "var(--coffee-bean)",
                            }}
                          >
                            WEIGHT TO SHIP (KG) *
                          </label>

                          {/* Quick Add Presets */}
                          <div style={{ display: "flex", gap: 6 }}>
                            <button
                              type="button"
                              onClick={() => handleQuickAdd(500)}
                              className="btn btn-outline"
                              style={{ padding: "2px 8px", fontSize: 11, height: "auto" }}
                            >
                              +500 kg
                            </button>
                            <button
                              type="button"
                              onClick={() => handleQuickAdd(1000)}
                              className="btn btn-outline"
                              style={{ padding: "2px 8px", fontSize: 11, height: "auto" }}
                            >
                              +1,000 kg
                            </button>
                            <button
                              type="button"
                              onClick={handleSetMax}
                              className="btn btn-outline"
                              style={{ padding: "2px 8px", fontSize: 11, height: "auto" }}
                            >
                              Max ({container.available_capacity_kg.toLocaleString()} kg)
                            </button>
                          </div>
                        </div>

                        <input
                          type="number"
                          step="any"
                          min="1"
                          max={container.available_capacity_kg}
                          placeholder={`Enter kg (1 to ${container.available_capacity_kg})`}
                          value={bookingCapacity}
                          onChange={(e) => {
                            setBookingCapacity(e.target.value);
                            if (bookingError) setBookingError("");
                          }}
                          required
                          disabled={bookingLoading}
                          style={{
                            width: "100%",
                            height: 46,
                            padding: "0 14px",
                            border: "1px solid var(--border)",
                            borderRadius: 8,
                            fontSize: 16,
                          }}
                        />
                      </div>

                      {/* Live Price Estimation Card */}
                      <div
                        style={{
                          background: "var(--white)",
                          border: "1px solid var(--border)",
                          borderRadius: 8,
                          padding: "12px 18px",
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          flexWrap: "wrap",
                          gap: 8,
                        }}
                      >
                        <div>
                          <span style={{ fontSize: 12, color: "var(--text-muted)", display: "block" }}>
                            Formula: Booked kg × Rate (₹{container.price_per_kg.toFixed(2)})
                          </span>
                          <span style={{ fontSize: 13, color: "var(--text-secondary)" }}>
                            Total Estimated Booking Amount:
                          </span>
                        </div>
                        <div style={{ textAlign: "right" }}>
                          <span
                            style={{
                              fontSize: 22,
                              fontWeight: 800,
                              color: estimatedTotal ? "var(--autumn-ember)" : "var(--text-muted)",
                            }}
                          >
                            ₹{estimatedTotal || "0.00"}
                          </span>
                        </div>
                      </div>

                      <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={
                          bookingLoading ||
                          !bookingCapacity ||
                          (complianceStatus && !complianceStatus.is_verified)
                        }
                        style={{
                          height: 48,
                          fontSize: 15,
                          fontWeight: 700,
                          width: "100%",
                        }}
                      >
                        {bookingLoading
                          ? "Reserving Space & Creating Booking..."
                          : complianceStatus && !complianceStatus.is_verified
                          ? "🔒 Verification Required to Book Space"
                          : `Reserve Space for ₹${estimatedTotal || "0.00"} →`}
                      </button>
                    </div>
                  </form>
                </div>
              ) : (
                <div
                  style={{
                    background: "#FEF2F2",
                    border: "1px solid #FECACA",
                    borderRadius: 12,
                    padding: "20px 24px",
                    marginBottom: 24,
                  }}
                >
                  <h4 style={{ margin: "0 0 6px", color: "#991B1B", fontSize: 16 }}>
                    Container Space Sold Out or Unavailable
                  </h4>
                  <p style={{ margin: "0 0 12px", fontSize: 13, color: "#7F1D1D" }}>
                    This container has reached its full capacity ({container.total_capacity_kg} kg)
                    or has been marked unavailable for booking.
                  </p>
                  <Link to="/containers" className="btn btn-outline btn-sm">
                    Search Other Available Containers →
                  </Link>
                </div>
              )}
            </>
          )}

          {/* =========================================================
              OWNING PROVIDER & ADMIN CONTROLS
          ========================================================= */}
          {isContainerOwner && (
            <div
              style={{
                marginTop: 20,
                paddingTop: 20,
                borderTop: "1px solid var(--border)",
              }}
            >
              <h4 style={{ margin: "0 0 12px", fontSize: 14, color: "var(--coffee-bean)", textTransform: "uppercase", letterSpacing: "0.5px" }}>
                Fleet Management (Owner Controls)
              </h4>

              <div className="container-actions">
                <Link to={`/containers/${container.container_id}/edit`} className="btn btn-outline">
                  ✏️ Edit Route & Pricing
                </Link>

                <button
                  onClick={handleToggleAvailability}
                  className={`btn ${container.is_available ? "btn-danger" : "btn-success"}`}
                >
                  {container.is_available ? "Mark Unavailable" : "Mark Available"}
                </button>

                <button
                  onClick={() => setShowDeleteModal(true)}
                  className="btn btn-danger"
                  style={{ marginLeft: "auto" }}
                >
                  🗑️ Delete Listing
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="confirm-overlay" onClick={() => setShowDeleteModal(false)}>
          <div className="confirm-box" onClick={(e) => e.stopPropagation()}>
            <h3>Delete Container Listing?</h3>
            <p>
              Are you sure you want to delete container #{container.container_id} ({container.origin} →{" "}
              {container.destination})? This action cannot be undone.
            </p>
            <div className="confirm-actions">
              <button
                type="button"
                className="btn btn-outline"
                onClick={() => setShowDeleteModal(false)}
                disabled={deleteLoading}
              >
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-danger"
                onClick={handleDelete}
                disabled={deleteLoading}
              >
                {deleteLoading ? "Deleting..." : "Yes, Delete Container"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContainerDetail;
