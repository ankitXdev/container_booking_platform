import { useState } from "react";
import { Link } from "react-router-dom";
import { searchContainers } from "../../services/containerService";
import "../../assets/dashboard.css";

/*
|--------------------------------------------------------------------------
| ContainerSearch
|--------------------------------------------------------------------------
| Public page. Calls GET /containers/ with optional filters.
| Results shown as cards linking to ContainerDetail.
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

const ContainerSearch = () => {
  const [filters, setFilters] = useState({
    origin: "",
    destination: "",
    min_capacity_kg: "",
  });

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  const isProvider = Boolean(localStorage.getItem("provider_id"));

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
    if (error) setError("");
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    setSearched(true);
    setResults([]);

    try {
      const data = await searchContainers(filters);
      setResults(data);
    } catch (err) {
      setError(err.message || "Failed to search containers.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFilters({ origin: "", destination: "", min_capacity_kg: "" });
    setResults([]);
    setSearched(false);
    setError("");
  };

  return (
    <div className="dashboard-page">

      {/* Page header */}
      <div className="page-header">
        <span className="page-eyebrow">MARKETPLACE</span>
        <h1>Browse Containers</h1>
        <p>
          Search available container space by route or minimum capacity.
          {isProvider && (
            <> &nbsp;
              <Link to="/containers/create" className="btn btn-primary btn-sm" style={{ marginLeft: 8 }}>
                + Add Container
              </Link>
            </>
          )}
        </p>
      </div>

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
                  <div className="container-route">
                    <span className="container-route-city">{c.origin}</span>
                    <span className="container-route-arrow">→</span>
                    <span className="container-route-city">{c.destination}</span>
                  </div>
                  <span className={`availability-badge ${c.is_available ? "available" : "unavailable"}`}>
                    {c.is_available ? "Available" : "Unavailable"}
                  </span>
                </div>

                {/* Stats */}
                <div className="container-card-stats">
                  <div className="container-stat">
                    <label>Available Capacity</label>
                    <p>{c.available_capacity_kg.toLocaleString()} kg</p>
                  </div>
                  <div className="container-stat">
                    <label>Price / kg</label>
                    <p>₹{c.price_per_kg}</p>
                  </div>
                  <div className="container-stat">
                    <label>Departure</label>
                    <p>{formatDate(c.departure_date)}</p>
                  </div>
                  <div className="container-stat">
                    <label>Total Capacity</label>
                    <p>{c.total_capacity_kg.toLocaleString()} kg</p>
                  </div>
                </div>

                {/* Footer */}
                <div className="container-card-footer">
                  <p className="container-provider-name">
                    Provider #{c.provider_id}
                  </p>
                  <Link
                    to={`/containers/${c.container_id}`}
                    className="btn btn-outline btn-sm"
                  >
                    View Details
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
