import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { createContainer } from "../../services/containerService";
import "../../assets/dashboard.css";

const CreateContainer = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    origin: "",
    destination: "",
    departure_date: "",
    total_capacity_kg: "",
    available_capacity_kg: "",
    price_per_kg: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      const updated = { ...prev, [name]: value };
      // auto-fill available capacity if total capacity is filled first and available is empty
      if (name === "total_capacity_kg" && !prev.available_capacity_kg) {
        updated.available_capacity_kg = value;
      }
      return updated;
    });
    if (error) setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const total = parseFloat(formData.total_capacity_kg);
    const available = parseFloat(formData.available_capacity_kg);
    const price = parseFloat(formData.price_per_kg);

    if (!formData.origin.trim() || !formData.destination.trim()) {
      setError("Origin and Destination are required.");
      return;
    }

    if (!formData.departure_date) {
      setError("Departure date is required.");
      return;
    }

    if (isNaN(total) || total <= 0) {
      setError("Total capacity must be a positive number.");
      return;
    }

    if (isNaN(available) || available <= 0) {
      setError("Available capacity must be a positive number.");
      return;
    }

    if (available > total) {
      setError("Available capacity cannot exceed total capacity.");
      return;
    }

    if (isNaN(price) || price <= 0) {
      setError("Price per kg must be greater than zero.");
      return;
    }

    setLoading(true);

    try {
      const result = await createContainer({
        origin: formData.origin.trim(),
        destination: formData.destination.trim(),
        departure_date: new Date(formData.departure_date).toISOString(),
        total_capacity_kg: total,
        available_capacity_kg: available,
        price_per_kg: price,
      });

      navigate(`/containers/${result.container_id}`);
    } catch (err) {
      setError(err.message || "Failed to create container listing.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <span className="page-eyebrow">LOGISTICS PROVIDER</span>
        <h1>Add Container Space</h1>
        <p>List available cargo space for exporters to search and book.</p>
      </div>

      <div className="profile-card" style={{ maxWidth: 650 }}>
        {error && <div className="feedback-error">{error}</div>}

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div className="form-group">
              <label style={{ display: "block", marginBottom: 6, fontSize: 12, fontWeight: 700, color: "var(--coffee-bean)" }}>
                ORIGIN PORT / CITY *
              </label>
              <input
                type="text"
                name="origin"
                placeholder="e.g. Mumbai (JNPT)"
                value={formData.origin}
                onChange={handleChange}
                required
                disabled={loading}
                style={{ width: "100%", height: 42, padding: "0 12px", border: "1px solid var(--border)", borderRadius: 8 }}
              />
            </div>

            <div className="form-group">
              <label style={{ display: "block", marginBottom: 6, fontSize: 12, fontWeight: 700, color: "var(--coffee-bean)" }}>
                DESTINATION PORT / CITY *
              </label>
              <input
                type="text"
                name="destination"
                placeholder="e.g. Dubai (Jebel Ali)"
                value={formData.destination}
                onChange={handleChange}
                required
                disabled={loading}
                style={{ width: "100%", height: 42, padding: "0 12px", border: "1px solid var(--border)", borderRadius: 8 }}
              />
            </div>
          </div>

          <div className="form-group">
            <label style={{ display: "block", marginBottom: 6, fontSize: 12, fontWeight: 700, color: "var(--coffee-bean)" }}>
              DEPARTURE DATE & TIME *
            </label>
            <input
              type="datetime-local"
              name="departure_date"
              value={formData.departure_date}
              onChange={handleChange}
              required
              disabled={loading}
              style={{ width: "100%", height: 42, padding: "0 12px", border: "1px solid var(--border)", borderRadius: 8 }}
            />
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div className="form-group">
              <label style={{ display: "block", marginBottom: 6, fontSize: 12, fontWeight: 700, color: "var(--coffee-bean)" }}>
                TOTAL CAPACITY (KG) *
              </label>
              <input
                type="number"
                name="total_capacity_kg"
                placeholder="e.g. 5000"
                step="any"
                min="1"
                value={formData.total_capacity_kg}
                onChange={handleChange}
                required
                disabled={loading}
                style={{ width: "100%", height: 42, padding: "0 12px", border: "1px solid var(--border)", borderRadius: 8 }}
              />
            </div>

            <div className="form-group">
              <label style={{ display: "block", marginBottom: 6, fontSize: 12, fontWeight: 700, color: "var(--coffee-bean)" }}>
                AVAILABLE CAPACITY (KG) *
              </label>
              <input
                type="number"
                name="available_capacity_kg"
                placeholder="e.g. 3000"
                step="any"
                min="1"
                value={formData.available_capacity_kg}
                onChange={handleChange}
                required
                disabled={loading}
                style={{ width: "100%", height: 42, padding: "0 12px", border: "1px solid var(--border)", borderRadius: 8 }}
              />
            </div>
          </div>

          <div className="form-group">
            <label style={{ display: "block", marginBottom: 6, fontSize: 12, fontWeight: 700, color: "var(--coffee-bean)" }}>
              PRICE PER KG (₹) *
            </label>
            <input
              type="number"
              name="price_per_kg"
              placeholder="e.g. 15.50"
              step="any"
              min="0.1"
              value={formData.price_per_kg}
              onChange={handleChange}
              required
              disabled={loading}
              style={{ width: "100%", height: 42, padding: "0 12px", border: "1px solid var(--border)", borderRadius: 8 }}
            />
          </div>

          <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
              style={{ height: 44, padding: "0 24px" }}
            >
              {loading ? "Publishing..." : "Publish Container Listing"}
            </button>
            <Link
              to="/containers"
              className="btn btn-outline"
              style={{ height: 44, display: "inline-flex", alignItems: "center" }}
            >
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateContainer;
