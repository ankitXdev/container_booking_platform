import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import {
  getContainerDetails,
  updateContainer,
} from "../../services/containerService";
import "../../assets/dashboard.css";

const EditContainer = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    origin: "",
    destination: "",
    departure_date: "",
    total_capacity_kg: "",
    available_capacity_kg: "",
    price_per_kg: "",
  });

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadContainer = async () => {
      try {
        const data = await getContainerDetails(id);
        // Format ISO date to YYYY-MM-DDTHH:MM for datetime-local input
        let dateVal = "";
        if (data.departure_date) {
          const d = new Date(data.departure_date);
          dateVal = d.toISOString().slice(0, 16);
        }

        setFormData({
          origin: data.origin || "",
          destination: data.destination || "",
          departure_date: dateVal,
          total_capacity_kg: data.total_capacity_kg || "",
          available_capacity_kg: data.available_capacity_kg || "",
          price_per_kg: data.price_per_kg || "",
        });
      } catch (err) {
        setError(err.message || "Failed to load container data.");
      } finally {
        setLoading(false);
      }
    };

    loadContainer();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
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

    if (isNaN(available) || available < 0) {
      setError("Available capacity must be 0 or greater.");
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

    setSubmitting(true);

    try {
      await updateContainer(id, {
        origin: formData.origin.trim(),
        destination: formData.destination.trim(),
        departure_date: new Date(formData.departure_date).toISOString(),
        total_capacity_kg: total,
        available_capacity_kg: available,
        price_per_kg: price,
      });

      navigate(`/containers/${id}`);
    } catch (err) {
      setError(err.message || "Failed to update container listing.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="empty-state">
          <h3>Loading container data...</h3>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div style={{ marginBottom: 16 }}>
        <Link to={`/containers/${id}`} className="btn btn-outline btn-sm">
          ← Cancel & Back
        </Link>
      </div>

      <div className="page-header">
        <span className="page-eyebrow">UPDATE LISTING</span>
        <h1>Edit Container #{id}</h1>
        <p>Modify route details, space availability, or pricing.</p>
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
                value={formData.origin}
                onChange={handleChange}
                required
                disabled={submitting}
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
                value={formData.destination}
                onChange={handleChange}
                required
                disabled={submitting}
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
              disabled={submitting}
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
                step="any"
                min="1"
                value={formData.total_capacity_kg}
                onChange={handleChange}
                required
                disabled={submitting}
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
                step="any"
                min="0"
                value={formData.available_capacity_kg}
                onChange={handleChange}
                required
                disabled={submitting}
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
              step="any"
              min="0.1"
              value={formData.price_per_kg}
              onChange={handleChange}
              required
              disabled={submitting}
              style={{ width: "100%", height: 42, padding: "0 12px", border: "1px solid var(--border)", borderRadius: 8 }}
            />
          </div>

          <div style={{ display: "flex", gap: 12, marginTop: 12 }}>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={submitting}
              style={{ height: 44, padding: "0 24px" }}
            >
              {submitting ? "Saving..." : "Save Changes"}
            </button>
            <Link
              to={`/containers/${id}`}
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

export default EditContainer;
