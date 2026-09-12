import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { searchContainers } from "../../services/containerService";
import useAuth from "../../hooks/useAuth";
import "../../assets/dashboard.css";

/*
|--------------------------------------------------------------------------
| ContainerSearch
|--------------------------------------------------------------------------
| Public page. Calls GET /containers/ with optional filters.
| Results shown as cards linking to ContainerDetail.
| Role-aware:
| - Exporters search available cargo space to book.
| - Providers can toggle between their own fleet and platform marketplace.
|--------------------------------------------------------------------------
*/

const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

/** Returns "green" | "amber" | "red" based on free percentage */
const capColor = (availPct) => {
  if (availPct > 50) return "green";
  if (availPct >= 20) return "amber";
  return "red";
};

/** Visual capacity bar component */
const CapacityBar = ({ total, available }) => {
  const bookedKg   = total - available;
  const freePct    = total > 0 ? Math.round((available / total) * 100) : 0;
  const filledPct  = 100 - freePct;
  const color      = capColor(freePct);

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
        <div className={`cap-bar-free ${color}`}   style={{ width: `${freePct}%`    }} title={`Free: ${available.toLocaleString()} kg`} />
      </div>
      <div className="cap-bar-legend">
        <span><span className={`cap-bar-dot ${color}`} />{available.toLocaleString()} kg free</span>
        <span><span className="cap-bar-dot grey" />{bookedKg.toLocaleString()} kg booked</span>
      </div>
    </div>
  );
};

/** Enhanced route display for card */
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
        📅 {formatDate(departureDate)}
      </span>
    )}
  </div>
);

const ContainerSearch = () => {
  const { user } = useAuth();
  const role = user?.role?.toLowerCase() || "exporter";
  const isProvider = role === "provider";
  const myProviderId = localStorage.getItem("provider_id");

  const [fleetScope, setFleetScope] = useState("all"); // "all" | "mine"
  const [filters, setFilters] = useState({
    origin: "",
    destination: "",
    min_capacity_kg: "",
  });

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  const executeSearch = async (scope, currentFilters) => {
    setError("");
    setLoading(true);
    setSearched(true);
    setResults([]);

    try {
      const searchParams = { ...currentFilters };
      if (scope === "mine" && myProviderId) {
        searchParams.provider_id = myProviderId;
      }
      const data = await searchContainers(searchParams);
      setResults(data);
    } catch (err) {
      setError(err.message || "Failed to search containers.");
    } finally {
      setLoading(false);
    }
  };

  // If provider switches scope tabs
  const handleScopeChange = (newScope) => {
    setFleetScope(newScope);
    executeSearch(newScope, filters);
  };

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
    if (error) setError("");
  };

  const handleSearch = (e) => {
    e.preventDefault();
    executeSearch(fleetScope, filters);
  };

  const handleReset = () => {
    const cleared = { origin: "", destination: "", min_capacity_kg: "" };
    setFilters(cleared);
    setResults([]);
    setSearched(false);
    setError("");
  };

  return (
    <div className="dashboard-page">

      {/* Page header */}
      <div className="page-header">
        <span className="page-eyebrow">
          {isProvider ? "FLEET & MARKETPLACE" : "MARKETPLACE"}
        </span>
        <h1>{isProvider ? "Container Fleet & Departures" : "Browse Containers"}</h1>
        <p>
          {isProvider
            ? "Inspect your published container voyages or explore marketplace departures."
            : "Search available container space by route or minimum capacity."}
          {isProvider && (
            <> &nbsp;
              <Link to="/containers/create" className="btn btn-primary btn-sm" style={{ marginLeft: 8 }}>
                + Add Container
              </Link>
            </>
          )}
        </p>
      </div>

      {/* Provider Fleet Scope Tabs */}
      {isProvider && myProviderId && (
        <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
          <button
            type="button"
            className={`btn btn-sm ${fleetScope === "all" ? "btn-primary" : "btn-outline"}`}
            onClick={() => handleScopeChange("all")}
          >
            🌐 All Marketplace Containers
          </button>
          <button
            type="button"
            className={`btn btn-sm ${fleetScope === "mine" ? "btn-primary" : "btn-outline"}`}
            onClick={() => handleScopeChange("mine")}
          >
            🚢 My Fleet Only
          </button>
        </div>
      )}

      {/* Filter bar */}
      <form onSubmit={handleSearch} className="filter-bar">
        <input
          name="origin"
          type="text"
          placeholder="Origin city"
          value={filters.origin}
          onChange={handleChange}
          disabled={loading}
        />
        <input
          name="destination"
          type="text"
          placeholder="Destination city"
          value={filters.destination}
          onChange={handleChange}
          disabled={loading}
        />
        <input
          name="min_capacity_kg"
          type="number"
          placeholder="Min capacity (kg)"
          min="0"
          value={filters.min_capacity_kg}
          onChange={handleChange}
          disabled={loading}
        />
        <div style={{ display: "flex", gap: 8, alignSelf: "end" }}>
          <button
            type="submit"
            className="btn btn-primary"
            style={{ height: 42 }}
            disabled={loading}
          >
            {loading ? "Searching..." : "Search"}
          </button>
          {searched && (
            <button
              type="button"
              className="btn btn-outline"
              style={{ height: 42 }}
              onClick={handleReset}
            >
              Reset
            </button>
          )}
        </div>
      </form>

      {/* Error */}
      {error && <div className="feedback-error">{error}</div>}

      {/* Pre-search hint */}
      {!searched && !error && (
        <div className="empty-state">
          <div className="empty-state-icon">🚢</div>
          <h3>Find container space</h3>
          <p>
            Use the filters above to search for available container capacity
            by origin, destination, or minimum weight.
          </p>
        </div>
      )}

      {/* No results */}
      {searched && !loading && results.length === 0 && !error && (
        <div className="empty-state">
          <div className="empty-state-icon">📭</div>
          <h3>No containers found</h3>
          <p>Try adjusting your filters or clearing them to see all available listings.</p>
        </div>
      )}

      {/* Results grid */}
      {results.length > 0 && (
        <>
          <p style={{ color: "var(--text-muted)", fontSize: 13, marginBottom: 16 }}>
            {results.length} listing{results.length !== 1 ? "s" : ""} found
          </p>

          <div className="container-cards">
            {results.map((c) => (
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
                    {" · "}
                    <Link
                      to={`/providers/${c.provider_id}`}
                      style={{ color: "var(--text-secondary)", textDecoration: "underline", fontSize: 12 }}
                    >
                      Provider #{c.provider_id}
                    </Link>
                  </p>
                  <Link
                    to={`/containers/${c.container_id}`}
                    className={`btn btn-sm ${role === "exporter" && c.is_available ? "btn-primary" : "btn-outline"}`}
                  >
                    {isProvider && myProviderId && String(c.provider_id) === String(myProviderId)
                      ? "Manage Fleet ⚙️"
                      : role === "exporter" && c.is_available
                      ? "Book Space →"
                      : "View Details →"}
                  </Link>
                </div>

              </div>
            ))}
          </div>
        </>
      )}

    </div>
  );
};

export default ContainerSearch;
