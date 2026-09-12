import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getProviderDetails } from "../../services/providerService";
import { searchContainers } from "../../services/containerService";
import "../../assets/dashboard.css";

/*
|--------------------------------------------------------------------------
| ProviderDetail  — Public Profile Page for Exporters
|--------------------------------------------------------------------------
| Route: /providers/:id
| Visible to: all authenticated users
| Shows: company info, performance stats, compliance badge, trade routes,
|        and the provider's active container fleet with capacity bars.
|--------------------------------------------------------------------------
*/

// ── Helpers ────────────────────────────────────────────────────────────────

const getInitials = (name) =>
  name ? name.slice(0, 2).toUpperCase() : "??";

const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

const formatDeparture = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

const capColor = (availPct) => {
  if (availPct > 50) return "green";
  if (availPct >= 20) return "amber";
  return "red";
};

// ── Sub-components ──────────────────────────────────────────────────────────

/** 4-box KPI metric grid */
const StatBox = ({ icon, value, label, sub }) => (
  <div
    style={{
      background: "var(--white)",
      border: "1px solid var(--border)",
      borderRadius: 12,
      padding: "18px 20px",
      display: "flex",
      flexDirection: "column",
      gap: 4,
    }}
  >
    <span style={{ fontSize: 24, lineHeight: 1 }}>{icon}</span>
    <p
      style={{
        margin: "6px 0 2px",
        fontSize: 22,
        fontWeight: 800,
        color: "var(--coffee-bean)",
        letterSpacing: "-0.5px",
      }}
    >
      {value}
    </p>
    <span style={{ fontSize: 12, fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.5px" }}>
      {label}
    </span>
    {sub && (
      <span style={{ fontSize: 11, color: "var(--text-secondary)" }}>{sub}</span>
    )}
  </div>
);

/** Visual capacity bar reused from ContainerSearch */
const CapacityBar = ({ total, available }) => {
  const bookedKg  = total - available;
  const freePct   = total > 0 ? Math.round((available / total) * 100) : 0;
  const filledPct = 100 - freePct;
  const color     = capColor(freePct);

  return (
    <div className="cap-bar-wrap">
      <div className="cap-bar-header">
        <span>Capacity</span>
        <span className={`cap-bar-pct ${color}`}>
          {freePct}% free — {available.toLocaleString()} kg of {total.toLocaleString()} kg
        </span>
      </div>
      <div className="cap-bar-track">
        <div className="cap-bar-filled" style={{ width: `${filledPct}%` }} title={`Booked: ${bookedKg.toLocaleString()} kg`} />
        <div className={`cap-bar-free ${color}`} style={{ width: `${freePct}%` }} title={`Free: ${available.toLocaleString()} kg`} />
      </div>
      <div className="cap-bar-legend">
        <span><span className={`cap-bar-dot ${color}`} />{available.toLocaleString()} kg free</span>
        <span><span className="cap-bar-dot grey" />{bookedKg.toLocaleString()} kg booked</span>
      </div>
    </div>
  );
};

/** Route display for container cards */
const RouteDisplay = ({ origin, destination, departureDate }) => (
  <div className="route-display">
    <div className="route-port">
      <span className="route-port-icon">🏭</span>
      <span className="route-port-name">{origin}</span>
      <span className="route-port-code">Origin</span>
    </div>
    <div className="route-mid">
      <span className="route-mid-ship">🚢</span>
      <div className="route-mid-line" />
    </div>
    <div className="route-port">
      <span className="route-port-icon">⚓</span>
      <span className="route-port-name">{destination}</span>
      <span className="route-port-code">Destination</span>
    </div>
    {departureDate && (
      <span className="route-date-pill">
        📅 {formatDeparture(departureDate)}
      </span>
    )}
  </div>
);

// ── Main Component ──────────────────────────────────────────────────────────

const ProviderDetail = () => {
  const { id } = useParams();

  const [provider, setProvider]     = useState(null);
  const [containers, setContainers] = useState([]);
  const [loading, setLoading]       = useState(true);
  const [fleetLoading, setFleetLoading] = useState(true);
  const [error, setError]           = useState("");

  // Load provider profile
  useEffect(() => {
    const fetchProvider = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await getProviderDetails(id);
        setProvider(data);
      } catch (err) {
        setError(err.message || "Failed to load provider profile.");
      } finally {
        setLoading(false);
      }
    };
    fetchProvider();
  }, [id]);

  // Load this provider's container fleet
  useEffect(() => {
    const fetchFleet = async () => {
      setFleetLoading(true);
      try {
        const data = await searchContainers({ provider_id: id });
        setContainers(data);
      } catch {
        // non-fatal — fleet section just stays empty
      } finally {
        setFleetLoading(false);
      }
    };
    fetchFleet();
  }, [id]);

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="empty-state">
          <div className="empty-state-icon">🔍</div>
          <h3>Loading provider profile...</h3>
          <p>Fetching logistics partner information.</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-page">
        <div className="feedback-error">{error}</div>
        <Link to="/providers/search" className="btn btn-outline" style={{ marginTop: 16 }}>
          ← Back to Provider Search
        </Link>
      </div>
    );
  }

  const memberSince = provider.created_at ? formatDate(provider.created_at) : "—";
  const cargoFormatted =
    provider.total_cargo_handled_kg >= 1000
      ? `${(provider.total_cargo_handled_kg / 1000).toFixed(1)}T`
      : `${provider.total_cargo_handled_kg.toLocaleString()} kg`;

  const activeFleet  = containers.filter((c) => c.is_available);
  const fullFleet    = containers;

  return (
    <div className="dashboard-page">

      {/* Breadcrumb */}
      <div style={{ marginBottom: 16 }}>
        <Link to="/providers/search" className="btn btn-outline btn-sm">
          ← Back to Provider Search
        </Link>
      </div>

      {/* ── Hero Header ──────────────────────────────────────── */}
      <div
        style={{
          background: "linear-gradient(135deg, var(--coffee-bean), var(--rich-mahogany))",
          borderRadius: 16,
          padding: "28px 32px",
          marginBottom: 24,
          display: "flex",
          alignItems: "flex-start",
          gap: 20,
          flexWrap: "wrap",
        }}
      >
        {/* Avatar */}
        <div
          style={{
            width: 72,
            height: 72,
            borderRadius: 15,
            background: "var(--autumn-ember)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 26,
            fontWeight: 800,
            color: "var(--white)",
            flexShrink: 0,
            boxShadow: "0 4px 14px rgba(183,79,13,0.4)",
          }}
        >
          {getInitials(provider.business_name)}
        </div>

        {/* Identity */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap", marginBottom: 6 }}>
            <h1
              style={{
                margin: 0,
                fontSize: 24,
                fontWeight: 800,
                color: "var(--white)",
                letterSpacing: "-0.3px",
              }}
            >
              {provider.business_name}
            </h1>
            <span
              style={{
                background: "#D1FAE5",
                color: "#065F46",
                fontSize: 10,
                fontWeight: 700,
                padding: "3px 10px",
                borderRadius: 20,
                letterSpacing: "0.5px",
                textTransform: "uppercase",
              }}
            >
              ✓ Approved Partner
            </span>
            {provider.compliance_verified && (
              <span
                style={{
                  background: "#EDE9FE",
                  color: "#5B21B6",
                  fontSize: 10,
                  fontWeight: 700,
                  padding: "3px 10px",
                  borderRadius: 20,
                  letterSpacing: "0.5px",
                  textTransform: "uppercase",
                }}
              >
                🔒 KYC Verified
              </span>
            )}
          </div>

          <div
            style={{
              display: "flex",
              gap: 18,
              flexWrap: "wrap",
              color: "#D8C7BD",
              fontSize: 13,
            }}
          >
            {provider.business_address && (
              <span>📍 {provider.business_address}</span>
            )}
            {provider.contact && (
              <span>📞 {provider.contact}</span>
            )}
            {provider.email && (
              <span>✉️ {provider.email}</span>
            )}
            <span>🗓 Member since {memberSince}</span>
          </div>
        </div>
      </div>

      {/* ── Stats Grid ───────────────────────────────────────── */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(190px, 1fr))",
          gap: 14,
          marginBottom: 24,
        }}
      >
        <StatBox
          icon="⚖️"
          value={cargoFormatted}
          label="Cargo Handled"
          sub="Confirmed bookings total"
        />
        <StatBox
          icon="📦"
          value={provider.completed_bookings_count}
          label="Completed Bookings"
          sub="Confirmed & fulfilled"
        />
        <StatBox
          icon="🚢"
          value={provider.active_containers_count}
          label="Active Fleet"
          sub={`${provider.total_containers_count} total containers`}
        />
        <StatBox
          icon="🗺️"
          value={provider.serviced_routes.length}
          label="Trade Routes"
          sub="Unique origin–destination pairs"
        />
      </div>

      {/* ── Trade Routes Panel ───────────────────────────────── */}
      {provider.serviced_routes.length > 0 && (
        <div
          style={{
            background: "var(--white)",
            border: "1px solid var(--border)",
            borderRadius: 14,
            padding: "20px 24px",
            marginBottom: 24,
          }}
        >
          <h3
            style={{
              margin: "0 0 14px",
              fontSize: 14,
              fontWeight: 700,
              color: "var(--coffee-bean)",
              textTransform: "uppercase",
              letterSpacing: "0.5px",
            }}
          >
            🗺️ Serviced Trade Routes
          </h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
            {provider.serviced_routes.map((route, idx) => (
              <div
                key={idx}
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 8,
                  padding: "7px 14px",
                  background: "#FFF7F1",
                  border: "1px solid rgba(183,79,13,0.2)",
                  borderRadius: 30,
                  fontSize: 12,
                  fontWeight: 600,
                  color: "var(--coffee-bean)",
                }}
              >
                <span>🏭</span>
                <span>{route.origin}</span>
                <span style={{ color: "var(--autumn-ember)" }}>→</span>
                <span>⚓</span>
                <span>{route.destination}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Compliance Card ──────────────────────────────────── */}
      <div
        style={{
          background: provider.compliance_verified ? "#ECFDF5" : "#FFFBEB",
          border: `1px solid ${provider.compliance_verified ? "#A7F3D0" : "#FCD34D"}`,
          borderRadius: 12,
          padding: "16px 20px",
          marginBottom: 24,
          display: "flex",
          alignItems: "center",
          gap: 14,
        }}
      >
        <span style={{ fontSize: 28, lineHeight: 1 }}>
          {provider.compliance_verified ? "✅" : "⚠️"}
        </span>
        <div>
          <p style={{ margin: "0 0 3px", fontWeight: 700, fontSize: 14, color: provider.compliance_verified ? "#065F46" : "#92400E" }}>
            {provider.compliance_verified
              ? "Verified Logistics Partner — All KYC & Compliance Documents Approved"
              : "Compliance Verification In Progress"}
          </p>
          <p style={{ margin: 0, fontSize: 12, color: provider.compliance_verified ? "#047857" : "#78350F" }}>
            {provider.compliance_verified
              ? "This provider has submitted and received admin approval for all required business registration and licensing documents."
              : "This provider has submitted compliance documents which are currently under admin review. Bookings may still proceed."}
          </p>
        </div>
      </div>

      {/* ── Active Fleet ─────────────────────────────────────── */}
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16, flexWrap: "wrap", gap: 10 }}>
          <h2 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: "var(--coffee-bean)" }}>
            🚢 Container Fleet
          </h2>
          {fullFleet.length > 0 && (
            <span style={{ fontSize: 12, color: "var(--text-muted)" }}>
              {activeFleet.length} active · {fullFleet.length - activeFleet.length} sold out / unavailable
            </span>
          )}
        </div>

        {fleetLoading ? (
          <div className="empty-state">
            <p>Loading fleet...</p>
          </div>
        ) : fullFleet.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📭</div>
            <h3>No active containers</h3>
            <p>This provider has no container listings on the platform right now.</p>
          </div>
        ) : (
          <div className="container-cards">
            {fullFleet.map((c) => (
              <div key={c.container_id} className="container-card">

                {/* Route + availability */}
                <div className="container-card-top">
                  <RouteDisplay
                    origin={c.origin}
                    destination={c.destination}
                    departureDate={c.departure_date}
                  />
                  <span className={`availability-badge ${c.is_available ? "available" : "unavailable"}`}>
                    {c.is_available ? "✓ Open" : "✕ Full"}
                  </span>
                </div>

                {/* Capacity visualizer */}
                <CapacityBar
                  total={c.total_capacity_kg}
                  available={c.available_capacity_kg}
                />

                {/* Footer */}
                <div className="container-card-footer">
                  <p className="container-provider-name">
                    <span style={{ fontWeight: 700, color: "var(--autumn-ember)" }}>
                      ₹{c.price_per_kg}/kg
                    </span>
                  </p>
                  <Link
                    to={`/containers/${c.container_id}`}
                    className={`btn btn-sm ${c.is_available ? "btn-primary" : "btn-outline"}`}
                  >
                    {c.is_available ? "Book Space →" : "View Details"}
                  </Link>
                </div>

              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
};

export default ProviderDetail;
