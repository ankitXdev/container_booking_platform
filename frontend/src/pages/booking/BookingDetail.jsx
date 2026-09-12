import { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import {
  getBookingDetails,
  cancelBooking,
  updateBookingStatus,
} from "../../services/bookingService";
import {
  createPaymentOrder,
  verifyPayment,
  getPaymentDetails,
} from "../../services/paymentService";
import useAuth from "../../hooks/useAuth";
import "../../assets/dashboard.css";

const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
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

// Helper to load external script dynamically (Razorpay checkout)
const loadRazorpayScript = () => {
  return new Promise((resolve) => {
    if (window.Razorpay) {
      resolve(true);
      return;
    }
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.onload = () => resolve(true);
    script.onerror = () => resolve(false);
    document.body.appendChild(script);
  });
};

const BookingDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const role = user?.role?.toLowerCase() || "exporter";

  const [booking, setBooking] = useState(null);
  const [payment, setPayment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionSuccess, setActionSuccess] = useState("");

  // Payment state
  const [payLoading, setPayLoading] = useState(false);

  // Cancel modal
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [cancelLoading, setCancelLoading] = useState(false);

  const fetchDetails = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getBookingDetails(id);
      setBooking(data);

      if (data.status === "confirmed") {
        try {
          const payData = await getPaymentDetails(id);
          setPayment(payData);
        } catch {
          // Payment details might not exist if manually confirmed
        }
      }
    } catch (err) {
      setError(err.message || "Failed to load booking details.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetails();
  }, [id]);

  const handlePayNow = async () => {
    setError("");
    setActionSuccess("");
    setPayLoading(true);

    try {
      const scriptLoaded = await loadRazorpayScript();
      if (!scriptLoaded) {
        throw new Error(
          "Failed to load Razorpay payment gateway. Please check your connection."
        );
      }

      // 1. Create order on backend
      const orderData = await createPaymentOrder(booking.booking_id);

      // 2. Configure Razorpay checkout options
      const options = {
        key: orderData.key_id,
        amount: orderData.amount_in_paise,
        currency: orderData.currency,
        name: "Cargo Booking Platform",
        description: `Space Booking #${booking.booking_id} (${booking.origin} → ${booking.destination})`,
        order_id: orderData.razorpay_order_id,
        prefill: {
          name: booking.exporter_name,
          email: booking.exporter_email,
        },
        theme: {
          color: "#B74F0D", // autumn-ember
        },
        handler: async function (response) {
          try {
            // 3. Verify signature on backend
            const verifyRes = await verifyPayment({
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
            });

            setActionSuccess("Payment completed successfully! Booking confirmed.");
            setBooking((prev) => ({ ...prev, status: "confirmed" }));

            // Fetch payment receipt
            const receipt = await getPaymentDetails(booking.booking_id);
            setPayment(receipt);
          } catch (vErr) {
            setError(vErr.message || "Payment verification failed.");
          }
        },
      };

      const razorpayInstance = new window.Razorpay(options);
      razorpayInstance.on("payment.failed", function (response) {
        setError(
          response.error?.description || "Payment failed or was cancelled."
        );
      });
      razorpayInstance.open();
    } catch (err) {
      setError(err.message || "Failed to initiate payment.");
    } finally {
      setPayLoading(false);
    }
  };

  const handleCancelBooking = async () => {
    setCancelLoading(true);
    setError("");
    setActionSuccess("");
    try {
      const res = await cancelBooking(booking.booking_id);
      setBooking((prev) => ({ ...prev, status: "cancelled" }));
      setActionSuccess("Booking has been cancelled and container capacity restored.");
      setShowCancelModal(false);
    } catch (err) {
      setError(err.message || "Failed to cancel booking.");
    } finally {
      setCancelLoading(false);
    }
  };

  const handleStatusChange = async (newStatus) => {
    setError("");
    setActionSuccess("");
    try {
      await updateBookingStatus(booking.booking_id, newStatus);
      setBooking((prev) => ({ ...prev, status: newStatus }));
      setActionSuccess(`Booking status updated to ${newStatus}.`);
    } catch (err) {
      setError(err.message || "Failed to update booking status.");
    }
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="empty-state">
          <h3>Loading booking information...</h3>
        </div>
      </div>
    );
  }

  if (error && !booking) {
    return (
      <div className="dashboard-page">
        <div className="feedback-error">{error}</div>
        <Link to="/bookings" className="btn btn-outline" style={{ marginTop: 16 }}>
          ← Back to Bookings
        </Link>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div style={{ marginBottom: 16 }}>
        <Link to="/bookings" className="btn btn-outline btn-sm">
          ← Back to Bookings
        </Link>
      </div>

      {actionSuccess && <div className="feedback-success">{actionSuccess}</div>}
      {error && <div className="feedback-error">{error}</div>}

      <div className="container-detail-card" style={{ maxWidth: 800 }}>
        {/* Header */}
        <div className="container-detail-header">
          <div className="container-detail-route">
            <span className="container-detail-city">{booking.origin}</span>
            <span className="container-detail-arrow">→</span>
            <span className="container-detail-city">{booking.destination}</span>
          </div>
          <div className="container-detail-meta">
            <span className={`status-badge ${getStatusBadgeClass(booking.status)}`}>
              {booking.status}
            </span>
            <span className="container-detail-date">
              Departure: {formatDate(booking.departure_date)}
            </span>
            <span className="container-detail-date">
              Booking #{booking.booking_id}
            </span>
          </div>
        </div>

        {/* Body */}
        <div className="container-detail-body">
          {/* Main Space & Price Metrics */}
          <div className="profile-grid" style={{ marginBottom: 24 }}>
            <div className="profile-field">
              <label>BOOKED CARGO WEIGHT</label>
              <p style={{ fontSize: 20, color: "var(--autumn-ember)", fontWeight: 700 }}>
                {booking.booked_capacity_kg.toLocaleString()} kg
              </p>
            </div>

            <div className="profile-field">
              <label>TOTAL AMOUNT</label>
              <p style={{ fontSize: 22, fontWeight: 800, color: "var(--coffee-bean)" }}>
                ₹{booking.total_price.toFixed(2)}
              </p>
            </div>

            <div className="profile-field">
              <label>RATE APPLIED</label>
              <p>₹{booking.price_per_kg?.toFixed(2)} / kg</p>
            </div>

            <div className="profile-field">
              <label>BOOKING DATE</label>
              <p>{formatDate(booking.created_at)}</p>
            </div>
          </div>

          {/* Parties involved */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 24 }}>
            <div
              style={{
                background: "var(--surface)",
                padding: "14px 18px",
                borderRadius: 10,
                border: "1px solid var(--border)",
              }}
            >
              <span style={{ fontSize: 10, fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase" }}>
                EXPORTER
              </span>
              <p style={{ margin: "4px 0 2px", fontWeight: 700, color: "var(--coffee-bean)", fontSize: 14 }}>
                {booking.exporter_name}
              </p>
              <p style={{ margin: 0, fontSize: 12, color: "var(--text-secondary)" }}>
                {booking.exporter_email}
              </p>
            </div>

            <div
              style={{
                background: "var(--surface)",
                padding: "14px 18px",
                borderRadius: 10,
                border: "1px solid var(--border)",
              }}
            >
              <span style={{ fontSize: 10, fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase" }}>
                LOGISTICS PROVIDER
              </span>
              <p style={{ margin: "4px 0 2px", fontWeight: 700, color: "var(--coffee-bean)", fontSize: 14 }}>
                {booking.provider_business_name}
              </p>
              <p style={{ margin: 0, fontSize: 12, color: "var(--text-secondary)" }}>
                Contact: {booking.provider_contact}
              </p>
            </div>
          </div>

          {/* Payment Section - Only for Exporter */}
          {role === "exporter" && booking.status === "pending" && (
            <div
              style={{
                background: "#FEF3C7",
                border: "1px solid #F59E0B",
                borderRadius: 12,
                padding: "20px 24px",
                marginBottom: 24,
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: 16,
                flexWrap: "wrap",
              }}
            >
              <div>
                <h4 style={{ margin: "0 0 4px", color: "#92400E", fontSize: 16 }}>
                  Payment Pending
                </h4>
                <p style={{ margin: 0, fontSize: 13, color: "#78350F" }}>
                  Complete online payment of <strong>₹{booking.total_price.toFixed(2)}</strong> via
                  Razorpay to secure and confirm your space reservation.
                </p>
              </div>

              <button
                type="button"
                className="btn btn-primary"
                onClick={handlePayNow}
                disabled={payLoading}
                style={{
                  height: 44,
                  padding: "0 28px",
                  fontSize: 14,
                  fontWeight: 700,
                  whiteSpace: "nowrap",
                }}
              >
                {payLoading ? "Connecting..." : `Pay ₹${booking.total_price.toFixed(2)}`}
              </button>
            </div>
          )}

          {/* Payment Receipt if confirmed */}
          {payment && (
            <div
              style={{
                background: "#F0FDF4",
                border: "1px solid #86EFAC",
                borderRadius: 12,
                padding: "20px 24px",
                marginBottom: 24,
              }}
            >
              <h4 style={{ margin: "0 0 10px", color: "#166534", fontSize: 16 }}>
                ✓ Payment Receipt & Transaction Info
              </h4>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, fontSize: 13 }}>
                <div>
                  <span style={{ color: "#15803D", fontWeight: 600 }}>Payment ID:</span>{" "}
                  <code>{payment.razorpay_payment_id || "N/A"}</code>
                </div>
                <div>
                  <span style={{ color: "#15803D", fontWeight: 600 }}>Order ID:</span>{" "}
                  <code>{payment.razorpay_order_id}</code>
                </div>
                <div>
                  <span style={{ color: "#15803D", fontWeight: 600 }}>Amount Paid:</span> ₹
                  {payment.amount?.toFixed(2)} {payment.currency}
                </div>
                <div>
                  <span style={{ color: "#15803D", fontWeight: 600 }}>Status:</span>{" "}
                  <strong style={{ textTransform: "uppercase" }}>{payment.status}</strong>
                </div>
              </div>
            </div>
          )}

          {/* Action Bar */}
          <div className="container-actions">
            {booking.status !== "cancelled" && (
              <button
                type="button"
                onClick={() => setShowCancelModal(true)}
                className="btn btn-danger"
              >
                Cancel Booking
              </button>
            )}

            {/* Provider manual status controls - Only shown to Logistics Providers / Admins */}
            {role !== "exporter" && (
              <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
                {booking.status === "pending" && (
                  <button
                    type="button"
                    onClick={() => handleStatusChange("confirmed")}
                    className="btn btn-outline btn-sm"
                  >
                    Mark Confirmed
                  </button>
                )}
                {booking.status !== "cancelled" && (
                  <button
                    type="button"
                    onClick={() => handleStatusChange("cancelled")}
                    className="btn btn-outline btn-sm"
                  >
                    Mark Cancelled
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Cancel Confirmation Modal */}
      {showCancelModal && (
        <div className="confirm-overlay" onClick={() => setShowCancelModal(false)}>
          <div className="confirm-box" onClick={(e) => e.stopPropagation()}>
            <h3>Cancel This Booking?</h3>
            <p>
              Are you sure you want to cancel booking #{booking.booking_id}? The booked space (
              {booking.booked_capacity_kg} kg) will be immediately restored to the container.
            </p>
            <div className="confirm-actions">
              <button
                type="button"
                className="btn btn-outline"
                onClick={() => setShowCancelModal(false)}
                disabled={cancelLoading}
              >
                Keep Booking
              </button>
              <button
                type="button"
                className="btn btn-danger"
                onClick={handleCancelBooking}
                disabled={cancelLoading}
              >
                {cancelLoading ? "Cancelling..." : "Yes, Cancel Booking"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BookingDetail;
