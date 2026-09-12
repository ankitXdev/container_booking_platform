import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { listBookings } from "../../services/bookingService";
import useAuth from "../../hooks/useAuth";
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
      return "status-approved";
    case "pending":
      return "status-pending";
    case "cancelled":
      return "status-rejected";
    default:
      return "";
  }
};

const BookingList = () => {
  const { user } = useAuth();
  const role = user?.role?.toLowerCase() || "exporter";
  const isProvider = role === "provider";
  const isAdmin = role === "admin";

  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchBookings = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await listBookings();
      setBookings(data);
    } catch (err) {
      setError(err.message || "Failed to load bookings.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <span className="page-eyebrow">
          {isAdmin ? "PLATFORM OPERATIONS" : isProvider ? "CUSTOMER ORDERS" : "ORDERS & SHIPMENTS"}
        </span>
        <h1>{isAdmin ? "All Platform Bookings" : isProvider ? "Customer Bookings" : "My Bookings"}</h1>
        <p>
          {isAdmin
            ? "Monitor and review all booking transactions across the platform."
            : isProvider
            ? "Manage cargo space reservations placed by exporters on your containers."
            : "Track your cargo container space bookings and payment statuses."}
        </p>
      </div>

      {error && <div className="feedback-error">{error}</div>}

      {loading ? (
        <div className="empty-state">
          <h3>Loading bookings...</h3>
        </div>
      ) : bookings.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">📦</div>
          <h3>No bookings found</h3>
          <p>
            {isProvider
              ? "No customer reservations have been made on your containers yet."
              : isAdmin
              ? "No booking transactions exist on the platform yet."
              : "You haven't booked any container space yet."}
          </p>
          {!isProvider && !isAdmin && (
            <Link to="/containers" className="btn btn-primary" style={{ marginTop: 16 }}>
              Browse Available Containers
            </Link>
          )}
        </div>
      ) : (
        <div className="container-cards">
          {bookings.map((b) => (
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
                <div className="container-stat">
                  <label>Departure Date</label>
                  <p>{formatDate(b.departure_date)}</p>
                </div>
                <div className="container-stat">
                  <label>Booked On</label>
                  <p>{formatDate(b.created_at)}</p>
                </div>
              </div>

              <div className="container-card-footer">
                <span style={{ fontSize: 12, color: "var(--text-muted)", fontWeight: 600 }}>
                  Booking #{b.booking_id}
                </span>
                <Link to={`/bookings/${b.booking_id}`} className="btn btn-primary btn-sm">
                  View & Manage
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BookingList;
