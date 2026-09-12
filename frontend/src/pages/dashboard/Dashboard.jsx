import { useState, useEffect } from "react";
import { Link, Navigate } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import { listBookings } from "../../services/bookingService";
import { searchContainers } from "../../services/containerService";
import {
  getExporterComplianceStatus,
  getProviderComplianceStatus,
} from "../../services/documentService";
import "../../assets/dashboard.css";

const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

const getStatusBadgeClass = (status) => {
  switch (status?.toLowerCase()) {
    case "confirmed":
    case "approved":
    case "verified":
      return "status-approved";
    case "pending":
      return "status-pending";
    case "cancelled":
    case "rejected":
      return "status-rejected";
    default:
      return "";
  }
};

const Dashboard = () => {
  const { user } = useAuth();
  const role = user?.role?.toLowerCase() || "exporter";

  // Admin redirect
  if (role === "admin") {
    return <Navigate to="/admin" replace />;
  }

  // State for exporter / provider overview data
  const [recentBookings, setRecentBookings] = useState([]);
  const [featuredContainers, setFeaturedContainers] = useState([]);
  const [compliance, setCompliance] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true);
      try {
        const compliancePromise =
          role === "provider"
            ? getProviderComplianceStatus()
            : getExporterComplianceStatus();

        const [bookingsData, containersData, complianceData] = await Promise.allSettled([
          listBookings(),
          searchContainers(),
          compliancePromise,
        ]);

        if (bookingsData.status === "fulfilled") {
          setRecentBookings(bookingsData.value.slice(0, 3));
        }

        if (containersData.status === "fulfilled") {
          setFeaturedContainers(containersData.value.slice(0, 3));
        }

        if (complianceData.status === "fulfilled") {
          setCompliance(complianceData.value);
        }
      } catch {
        // Soft fail
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, [role]);

  return (
    <div className="dashboard-page">
      {/* =========================================================
          EXPORTER DASHBOARD VIEW
      ========================================================= */}
      {role === "exporter" && (
        <div>
          <div className="page-header">
            <span className="page-eyebrow">EXPORTER WORKSPACE</span>
            <h1>Welcome back, {user?.name || "Exporter"}</h1>
            <p>
              Search available cargo space in shipping containers, manage your freight bookings,
              and process instant online payments.
            </p>
          </div>

          {/* Compliance Status Alert for Exporter */}
          {compliance && !compliance.is_verified && (
            <div
              style={{
                background: compliance.status === "PENDING" ? "#FFFBEB" : "#FEF2F2",
                borderLeft: `5px solid ${compliance.status === "PENDING" ? "#D97706" : "#DC2626"}`,
                borderRadius: 8,
                padding: "16px 20px",
                marginBottom: 24,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                flexWrap: "wrap",
                gap: 12,
              }}
            >
              <div>
                <strong style={{ color: compliance.status === "PENDING" ? "#92400E" : "#991B1B", fontSize: 14 }}>
                  {compliance.status === "PENDING"
                    ? "⏳ Account Verification In Progress"
                    : "⚠️ Document Verification Required"}
                </strong>
                <p style={{ margin: "4px 0 0", fontSize: 13, color: "var(--text-secondary)" }}>
                  {compliance.message}
                </p>
              </div>
              <Link to="/documents" className="btn btn-outline btn-sm">
                Upload / View Documents →
              </Link>
            </div>
          )}

          {/* Action Cards for Exporter */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
              gap: 16,
              marginBottom: 32,
            }}
          >
            <div
              className="container-card"
              style={{
                borderLeft: "4px solid var(--autumn-ember)",
                background: "linear-gradient(135deg, #FFFFFF, #FFFBF7)",
              }}
            >
              <div style={{ fontSize: 24, marginBottom: 8 }}>🚢</div>
              <h3 style={{ margin: "0 0 6px", fontSize: 17, color: "var(--coffee-bean)" }}>
                Find Container Space
              </h3>
              <p style={{ margin: "0 0 16px", fontSize: 13, color: "var(--text-secondary)" }}>
                Browse routes and reserve partially filled container space at competitive rates.
              </p>
              <Link to="/containers" className="btn btn-primary btn-sm">
                Browse Marketplace →
              </Link>
            </div>

            <div
              className="container-card"
              style={{
                borderLeft: "4px solid #059669",
                background: "linear-gradient(135deg, #FFFFFF, #F0FDF4)",
              }}
            >
              <div style={{ fontSize: 24, marginBottom: 8 }}>📦</div>
              <h3 style={{ margin: "0 0 6px", fontSize: 17, color: "var(--coffee-bean)" }}>
                My Active Shipments
              </h3>
              <p style={{ margin: "0 0 16px", fontSize: 13, color: "var(--text-secondary)" }}>
                Track payment confirmation, booked cargo weight, and departure schedules.
              </p>
              <Link to="/bookings" className="btn btn-outline btn-sm">
                View My Bookings ({recentBookings.length}) →
              </Link>
            </div>

            <div
              className="container-card"
              style={{
                borderLeft: "4px solid #2563EB",
                background: "linear-gradient(135deg, #FFFFFF, #EFF6FF)",
              }}
            >
              <div style={{ fontSize: 24, marginBottom: 8 }}>🏢</div>
              <h3 style={{ margin: "0 0 6px", fontSize: 17, color: "var(--coffee-bean)" }}>
                Logistics Providers
              </h3>
              <p style={{ margin: "0 0 16px", fontSize: 13, color: "var(--text-secondary)" }}>
                Search and connect with admin-verified freight forwarders and shipping partners.
              </p>
              <Link to="/providers/search" className="btn btn-outline btn-sm">
                Search Providers →
              </Link>
            </div>
          </div>

          {/* Recent Bookings Section */}
          <div style={{ marginBottom: 32 }}>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: 16,
              }}
            >
              <h2 style={{ fontSize: 20, color: "var(--coffee-bean)", margin: 0 }}>
                Recent Bookings
              </h2>
              <Link to="/bookings" style={{ fontSize: 13, color: "var(--autumn-ember)", fontWeight: 700 }}>
                View All Bookings →
              </Link>
            </div>

            {loading ? (
              <div className="empty-state">
                <p>Loading your shipments...</p>
              </div>
            ) : recentBookings.length === 0 ? (
              <div className="empty-state" style={{ padding: "28px" }}>
                <p style={{ margin: 0 }}>
                  You don't have any bookings yet.{" "}
                  <Link to="/containers" style={{ color: "var(--autumn-ember)", fontWeight: 700 }}>
                    Search available containers
                  </Link>{" "}
                  to reserve space.
                </p>
              </div>
            ) : (
              <div className="container-cards">
                {recentBookings.map((b) => (
                  <div key={b.booking_id} className="container-card">
                    <div className="container-card-top">
                      <div className="container-route">
                        <span className="container-route-city">{b.origin}</span>
                        <span className="container-route-arrow">→</span>
                        <span className="container-route-city">{b.destination}</span>
                      </div>
                      <span className={`status-badge ${getStatusBadgeClass(b.status)}`}>
                        {b.status}
                      </span>
                    </div>

                    <div className="container-card-stats">
                      <div className="container-stat">
                        <label>Booked Space</label>
                        <p>{b.booked_capacity_kg.toLocaleString()} kg</p>
                      </div>
                      <div className="container-stat">
                        <label>Total Price</label>
                        <p style={{ color: "var(--autumn-ember)", fontWeight: 700 }}>
                          ₹{b.total_price.toFixed(2)}
                        </p>
                      </div>
                    </div>

                    <div className="container-card-footer">
                      <span style={{ fontSize: 12, color: "var(--text-muted)" }}>
                        Departs: {formatDate(b.departure_date)}
                      </span>
                      <Link to={`/bookings/${b.booking_id}`} className="btn btn-primary btn-sm">
                        {b.status === "pending" ? "Pay Now" : "Details"}
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Available Containers Preview */}
          <div>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: 16,
              }}
            >
              <h2 style={{ fontSize: 20, color: "var(--coffee-bean)", margin: 0 }}>
                Popular Container Departures
              </h2>
              <Link to="/containers" style={{ fontSize: 13, color: "var(--autumn-ember)", fontWeight: 700 }}>
                Explore All Containers →
              </Link>
            </div>

            <div className="container-cards">
              {featuredContainers.map((c) => (
                <div key={c.container_id} className="container-card">
                  <div className="container-card-top">
                    <div className="container-route">
                      <span className="container-route-city">{c.origin}</span>
                      <span className="container-route-arrow">→</span>
                      <span className="container-route-city">{c.destination}</span>
                    </div>
                    <span className="availability-badge available">Available</span>
                  </div>

                  <div className="container-card-stats">
                    <div className="container-stat">
                      <label>Available Space</label>
                      <p>{c.available_capacity_kg.toLocaleString()} kg</p>
                    </div>
                    <div className="container-stat">
                      <label>Price / kg</label>
                      <p>₹{c.price_per_kg}</p>
                    </div>
                  </div>

                  <div className="container-card-footer">
                    <span style={{ fontSize: 12, color: "var(--text-muted)" }}>
                      Departure: {formatDate(c.departure_date)}
                    </span>
                    <Link to={`/containers/${c.container_id}`} className="btn btn-outline btn-sm">
                      Book Space
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* =========================================================
          LOGISTICS PROVIDER DASHBOARD VIEW
      ========================================================= */}
      {role === "provider" && (
        <div>
          <div className="page-header">
            <span className="page-eyebrow">PROVIDER COMMAND CENTER</span>
            <h1>Welcome, {user?.name || "Logistics Partner"}</h1>
            <p>
              List available cargo space in your shipping containers, manage reservations made by exporters,
              and maintain your logistics company profile.
            </p>
          </div>

          {/* Compliance Status Alert for Provider */}
          {compliance && !compliance.is_verified && (
            <div
              style={{
                background: compliance.status === "PENDING" ? "#FFFBEB" : "#FEF2F2",
                borderLeft: `5px solid ${compliance.status === "PENDING" ? "#D97706" : "#DC2626"}`,
                borderRadius: 8,
                padding: "16px 20px",
                marginBottom: 24,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                flexWrap: "wrap",
                gap: 12,
              }}
            >
              <div>
                <strong style={{ color: compliance.status === "PENDING" ? "#92400E" : "#991B1B", fontSize: 14 }}>
                  {compliance.status === "PENDING"
                    ? "⏳ Provider Account Pending Approval"
                    : "⚠️ Provider Profile / Documents Required"}
                </strong>
                <p style={{ margin: "4px 0 0", fontSize: 13, color: "var(--text-secondary)" }}>
                  {compliance.message || "Submit licenses to allow container publishing."}
                </p>
              </div>
              <Link to="/documents" className="btn btn-outline btn-sm">
                Manage Documents & Licenses →
              </Link>
            </div>
          )}

          {/* Action Cards for Provider */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
              gap: 16,
              marginBottom: 32,
            }}
          >
            <div
              className="container-card"
              style={{
                borderLeft: "4px solid var(--autumn-ember)",
                background: "linear-gradient(135deg, #FFFFFF, #FFFBF7)",
              }}
            >
              <div style={{ fontSize: 24, marginBottom: 8 }}>➕</div>
              <h3 style={{ margin: "0 0 6px", fontSize: 17, color: "var(--coffee-bean)" }}>
                Add Container Space
              </h3>
              <p style={{ margin: "0 0 16px", fontSize: 13, color: "var(--text-secondary)" }}>
                Publish newly scheduled shipping routes, departure dates, and weight capacities.
              </p>
              <Link to="/containers/create" className="btn btn-primary btn-sm">
                + Create Container Listing
              </Link>
            </div>

            <div
              className="container-card"
              style={{
                borderLeft: "4px solid #059669",
                background: "linear-gradient(135deg, #FFFFFF, #F0FDF4)",
              }}
            >
              <div style={{ fontSize: 24, marginBottom: 8 }}>📋</div>
              <h3 style={{ margin: "0 0 6px", fontSize: 17, color: "var(--coffee-bean)" }}>
                Container Fleet
              </h3>
              <p style={{ margin: "0 0 16px", fontSize: 13, color: "var(--text-secondary)" }}>
                View, update capacities, edit pricing, or toggle availability on existing listings.
              </p>
              <Link to="/containers" className="btn btn-outline btn-sm">
                Manage Containers →
              </Link>
            </div>

            <div
              className="container-card"
              style={{
                borderLeft: "4px solid #2563EB",
                background: "linear-gradient(135deg, #FFFFFF, #EFF6FF)",
              }}
            >
              <div style={{ fontSize: 24, marginBottom: 8 }}>📥</div>
              <h3 style={{ margin: "0 0 6px", fontSize: 17, color: "var(--coffee-bean)" }}>
                Customer Bookings
              </h3>
              <p style={{ margin: "0 0 16px", fontSize: 13, color: "var(--text-secondary)" }}>
                Review reservations placed by exporters on your scheduled departures.
              </p>
              <Link to="/bookings" className="btn btn-outline btn-sm">
                View Incoming Bookings →
              </Link>
            </div>

            <div
              className="container-card"
              style={{
                borderLeft: "4px solid #7C3AED",
                background: "linear-gradient(135deg, #FFFFFF, #F5F3FF)",
              }}
            >
              <div style={{ fontSize: 24, marginBottom: 8 }}>🏢</div>
              <h3 style={{ margin: "0 0 6px", fontSize: 17, color: "var(--coffee-bean)" }}>
                Company Profile
              </h3>
              <p style={{ margin: "0 0 16px", fontSize: 13, color: "var(--text-secondary)" }}>
                Verify your business credentials, contact phone, and company address.
              </p>
              <Link to="/provider/profile" className="btn btn-outline btn-sm">
                View Business Profile →
              </Link>
            </div>
          </div>

          {/* Quick Shortcuts & Guidance */}
          <div
            style={{
              background: "var(--surface)",
              borderRadius: 12,
              padding: "20px 24px",
              border: "1px solid var(--border)",
            }}
          >
            <h3 style={{ margin: "0 0 8px", fontSize: 16, color: "var(--coffee-bean)" }}>
              💡 Operational Guidelines for Logistics Providers
            </h3>
            <ul style={{ margin: 0, paddingLeft: 20, fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.8 }}>
              <li>
                Containers must be listed with realistic <code>departure_date</code> schedules and maximum <code>total_capacity_kg</code>.
              </li>
              <li>
                When exporters book space, the available capacity decreases automatically. Once it reaches 0 kg, the container is marked unavailable.
              </li>
              <li>
                You can review customer bookings under <strong>Customer Bookings</strong> and manually confirm or cancel if needed.
              </li>
              <li>
                Ensure your company profile has verified contact details so exporters can reach you with shipping documents.
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
