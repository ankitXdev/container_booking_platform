import { useState } from "react";
import { searchProviders } from "../../services/providerService";
import "../../assets/dashboard.css";

/*
|--------------------------------------------------------------------------
| SearchProviders
|--------------------------------------------------------------------------
| Calls GET /providers/?business_name=...
| Displays a list of provider cards with name, address, contact, and
| approval status badge.
|--------------------------------------------------------------------------
*/

const getInitials = (name) =>
  name ? name[0].toUpperCase() : "P";

const SearchProviders = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();

    const trimmed = query.trim();
    if (!trimmed) return;

    setError("");
    setLoading(true);
    setSearched(true);
    setResults([]);

    try {
      const data = await searchProviders(trimmed);
      setResults(data);
    } catch (err) {
      setError(err.message || "Failed to search providers.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-page">

      {/* Page header */}
      <div className="page-header">
        <span className="page-eyebrow">DISCOVERY</span>
        <h1>Search Providers</h1>
        <p>Find verified logistics providers by business name.</p>
      </div>

      {/* Search bar */}
      <form onSubmit={handleSearch} className="search-bar-wrapper">
        <input
          type="text"
          placeholder="Enter a business name..."
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            if (error) setError("");
          }}
          disabled={loading}
          aria-label="Search providers"
        />
        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || !query.trim()}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {/* Error */}
      {error && (
        <div className="feedback-error">{error}</div>
      )}

      {/* Pre-search hint */}
      {!searched && !error && (
        <div className="empty-state">
          <div className="empty-state-icon">🔍</div>
          <h3>Find a provider</h3>
          <p>
            Type a business name above to search for approved
            logistics providers on the platform.
          </p>
        </div>
      )}

      {/* No results */}
      {searched && !loading && results.length === 0 && !error && (
        <div className="empty-state">
          <div className="empty-state-icon">📭</div>
          <h3>No providers found</h3>
          <p>
            No providers matched &ldquo;{query}&rdquo;. Try a
            different business name.
          </p>
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div className="provider-cards">
          {results.map((provider) => (
            <div
              key={provider.provider_id}
              className="provider-card"
            >
              <div className="provider-card-avatar">
                {getInitials(provider.business_name)}
              </div>

              <div className="provider-card-body">
                <h3 className="provider-card-name">
                  {provider.business_name}
                </h3>

                <div className="provider-card-meta">
                  {provider.business_address && (
                    <span>📍 {provider.business_address}</span>
                  )}
                  {provider.contact && (
                    <span>📞 {provider.contact}</span>
                  )}
                </div>
              </div>

              {provider.approval_status && (
                <span
                  className={`status-badge ${provider.approval_status.toLowerCase()}`}
                >
                  {provider.approval_status}
                </span>
              )}
            </div>
          ))}
        </div>
      )}

    </div>
  );
};

export default SearchProviders;
