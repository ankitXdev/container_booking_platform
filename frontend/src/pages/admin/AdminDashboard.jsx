import { useState, useEffect } from "react";
import {
  getPlatformStats,
  getPendingProviders,
  approveProvider,
  rejectProvider,
  getAllBookings,
} from "../../services/adminService";
import {
  getAllDocumentsForAdmin,
  reviewExporterDocument,
  reviewProviderDocument,
} from "../../services/documentService";
import "../../assets/dashboard.css";

const API_BASE = import.meta.env.VITE_API_URL;

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

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [pendingProviders, setPendingProviders] = useState([]);
  const [allBookings, setAllBookings] = useState([]);
  const [documentsData, setDocumentsData] = useState({ exporter_documents: [], provider_documents: [] });
  const [activeTab, setActiveTab] = useState("overview"); // overview | providers | bookings | documents

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionSuccess, setActionSuccess] = useState("");

  const [actionLoadingId, setActionLoadingId] = useState(null);
  const [rejectionModal, setRejectionModal] = useState(null); // { type: 'exporter' | 'provider', id: number }
  const [rejectionReason, setRejectionReason] = useState("");

  const fetchAdminData = async () => {
    setLoading(true);
    setError("");
    try {
      const [statsData, providersData, bookingsData, docsData] = await Promise.all([
        getPlatformStats(),
        getPendingProviders(),
        getAllBookings(),
        getAllDocumentsForAdmin().catch(() => ({ exporter_documents: [], provider_documents: [] })),
      ]);
      setStats(statsData);
      setPendingProviders(providersData);
      setAllBookings(bookingsData);
      setDocumentsData(docsData);
    } catch (err) {
      setError(err.message || "Failed to load admin dashboard data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
  }, []);

  const handleApprove = async (providerId) => {
    setActionLoadingId(providerId);
    setActionSuccess("");
    setError("");
    try {
      await approveProvider(providerId);
      setActionSuccess(`Provider #${providerId} approved successfully!`);
      // Update pending list
      setPendingProviders((prev) =>
        prev.filter((p) => p.provider_id !== providerId)
      );
      // Refresh stats
      const newStats = await getPlatformStats();
      setStats(newStats);
    } catch (err) {
      setError(err.message || "Failed to approve provider.");
    } finally {
      setActionLoadingId(null);
    }
  };

  const handleReject = async (providerId) => {
    setActionLoadingId(providerId);
    setActionSuccess("");
    setError("");
    try {
      await rejectProvider(providerId);
      setActionSuccess(`Provider #${providerId} rejected.`);
      // Update pending list
      setPendingProviders((prev) =>
        prev.filter((p) => p.provider_id !== providerId)
      );
      // Refresh stats
      const newStats = await getPlatformStats();
      setStats(newStats);
    } catch (err) {
      setError(err.message || "Failed to reject provider.");
    } finally {
      setActionLoadingId(null);
    }
  };

  const handleReviewDoc = async (type, documentId, status, rejectionNote = null) => {
    setActionLoadingId(`${type}-${documentId}`);
    setActionSuccess("");
    setError("");
    try {
      if (type === "exporter") {
        await reviewExporterDocument(documentId, {
          status,
          rejection_reason: rejectionNote,
        });
      } else {
        await reviewProviderDocument(documentId, {
          status,
          rejection_reason: rejectionNote,
        });
      }

      setActionSuccess(`Document #${documentId} marked as ${status}!`);
      // Refresh documents
      const docsData = await getAllDocumentsForAdmin();
      setDocumentsData(docsData);
      setRejectionModal(null);
      setRejectionReason("");
    } catch (err) {
      setError(err.message || "Failed to update document status.");
    } finally {
      setActionLoadingId(null);
    }
  };

  const totalPendingDocs =
    (documentsData.exporter_documents?.filter((d) => d.status === "PENDING").length || 0) +
    (documentsData.provider_documents?.filter((d) => d.status === "PENDING").length || 0);

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="empty-state">
          <h3>Loading platform administration...</h3>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <span className="page-eyebrow">PLATFORM GOVERNANCE</span>
        <h1>Admin Console</h1>
        <p>Monitor platform operations, verify compliance documents, approve logistics providers, and supervise bookings.</p>
      </div>

      {actionSuccess && <div className="feedback-success">{actionSuccess}</div>}
      {error && <div className="feedback-error">{error}</div>}

      {/* Navigation Tabs */}
      <div style={{ display: "flex", gap: 12, marginBottom: 24, borderBottom: "1px solid var(--border)", paddingBottom: 12 }}>
        <button
          type="button"
          onClick={() => setActiveTab("overview")}
          className={`btn ${activeTab === "overview" ? "btn-primary" : "btn-outline"} btn-sm`}
        >
          Overview & Stats
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("documents")}
          className={`btn ${activeTab === "documents" ? "btn-primary" : "btn-outline"} btn-sm`}
        >
          Document Verification ({totalPendingDocs} Pending)
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("providers")}
          className={`btn ${activeTab === "providers" ? "btn-primary" : "btn-outline"} btn-sm`}
        >
          Pending Providers ({pendingProviders.length})
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("bookings")}
          className={`btn ${activeTab === "bookings" ? "btn-primary" : "btn-outline"} btn-sm`}
        >
          All System Bookings ({allBookings.length})
        </button>
      </div>

      {/* TAB 1: OVERVIEW & STATS */}
      {activeTab === "overview" && stats && (
        <div>
          {/* High-level metrics */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
              gap: 16,
              marginBottom: 24,
            }}
          >
            <div className="container-stat" style={{ padding: "18px 20px", background: "var(--white)", border: "1px solid var(--border)" }}>
              <label>TOTAL REVENUE</label>
              <p style={{ fontSize: 24, color: "var(--autumn-ember)", fontWeight: 800 }}>
                ₹{stats.total_revenue?.toLocaleString("en-IN", { minimumFractionDigits: 2 })}
              </p>
            </div>

            <div className="container-stat" style={{ padding: "18px 20px", background: "var(--white)", border: "1px solid var(--border)" }}>
              <label>TOTAL PLATFORM USERS</label>
              <p style={{ fontSize: 24, fontWeight: 700 }}>{stats.total_users}</p>
              <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
                {stats.total_exporters} Exporters · {stats.total_providers} Providers
              </span>
            </div>

            <div className="container-stat" style={{ padding: "18px 20px", background: "var(--white)", border: "1px solid var(--border)" }}>
              <label>CONTAINERS LISTED</label>
              <p style={{ fontSize: 24, fontWeight: 700 }}>{stats.containers?.total}</p>
              <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
                {stats.containers?.available} Available · {stats.containers?.unavailable} Filled/Unavailable
              </span>
            </div>

            <div className="container-stat" style={{ padding: "18px 20px", background: "var(--white)", border: "1px solid var(--border)" }}>
              <label>TOTAL BOOKINGS</label>
              <p style={{ fontSize: 24, fontWeight: 700 }}>{stats.bookings?.total}</p>
              <span style={{ fontSize: 11, color: "var(--text-muted)" }}>
                {stats.bookings?.confirmed} Confirmed · {stats.bookings?.pending} Pending · {stats.bookings?.cancelled} Cancelled
              </span>
            </div>
          </div>

          {/* Provider Approval Status Cards */}
          <div className="profile-card" style={{ maxWidth: "100%", marginBottom: 24 }}>
            <h3 style={{ margin: "0 0 16px", fontSize: 17, color: "var(--coffee-bean)" }}>
              Provider Verification Overview
            </h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 14 }}>
              <div className="container-stat">
                <label>TOTAL PROVIDERS</label>
                <p>{stats.providers?.total}</p>
              </div>
              <div className="container-stat">
                <label>APPROVED</label>
                <p style={{ color: "#065F46" }}>{stats.providers?.approved}</p>
              </div>
              <div className="container-stat">
                <label>PENDING REVIEW</label>
                <p style={{ color: "#D97706" }}>{stats.providers?.pending}</p>
              </div>
              <div className="container-stat">
                <label>REJECTED</label>
                <p style={{ color: "#DC2626" }}>{stats.providers?.rejected}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: DOCUMENT VERIFICATION */}
      {activeTab === "documents" && (
        <div>
          {/* Exporter Documents */}
          <div className="profile-card" style={{ maxWidth: "100%", marginBottom: 32 }}>
            <h3 style={{ margin: "0 0 16px", fontSize: 18, color: "var(--coffee-bean)" }}>
              🚢 Exporter Documents ({documentsData.exporter_documents?.length || 0})
            </h3>
            {(!documentsData.exporter_documents || documentsData.exporter_documents.length === 0) ? (
              <p style={{ color: "var(--text-secondary)", margin: 0 }}>No exporter documents uploaded yet.</p>
            ) : (
              <div className="table-responsive">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Exporter</th>
                      <th>Type</th>
                      <th>Doc Number</th>
                      <th>Uploaded</th>
                      <th>Status</th>
                      <th>File Link</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {documentsData.exporter_documents.map((doc) => (
                      <tr key={doc.document_id}>
                        <td>#{doc.document_id}</td>
                        <td>
                          <strong>{doc.user_name || "Exporter"}</strong>
                          <div style={{ fontSize: 11, color: "var(--text-secondary)" }}>{doc.user_email}</div>
                        </td>
                        <td><span style={{ fontWeight: 600 }}>{doc.document_type}</span></td>
                        <td>{doc.document_number || "—"}</td>
                        <td>{formatDate(doc.uploaded_at)}</td>
                        <td>
                          <span className={`status-badge ${getStatusBadgeClass(doc.status)}`}>
                            {doc.status}
                          </span>
                        </td>
                        <td>
                          <a
                            href={`${API_BASE}${doc.document_url}`}
                            target="_blank"
                            rel="noreferrer"
                            className="btn btn-outline btn-sm"
                            style={{ padding: "3px 8px", fontSize: 11 }}
                          >
                            View File ↗
                          </a>
                        </td>
                        <td>
                          {doc.status === "PENDING" ? (
                            <div style={{ display: "flex", gap: 6 }}>
                              <button
                                type="button"
                                onClick={() => handleReviewDoc("exporter", doc.document_id, "VERIFIED")}
                                disabled={actionLoadingId === `exporter-${doc.document_id}`}
                                className="btn btn-success btn-sm"
                                style={{ padding: "4px 8px", fontSize: 11 }}
                              >
                                ✓ Verify
                              </button>
                              <button
                                type="button"
                                onClick={() => setRejectionModal({ type: "exporter", id: doc.document_id })}
                                disabled={actionLoadingId === `exporter-${doc.document_id}`}
                                className="btn btn-danger btn-sm"
                                style={{ padding: "4px 8px", fontSize: 11 }}
                              >
                                ✕ Reject
                              </button>
                            </div>
                          ) : (
                            <span style={{ fontSize: 12, color: "var(--text-muted)" }}>
                              {doc.rejection_reason ? `Rejected: ${doc.rejection_reason}` : "Reviewed"}
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Provider Documents */}
          <div className="profile-card" style={{ maxWidth: "100%", marginBottom: 24 }}>
            <h3 style={{ margin: "0 0 16px", fontSize: 18, color: "var(--coffee-bean)" }}>
              🏢 Provider Documents ({documentsData.provider_documents?.length || 0})
            </h3>
            {(!documentsData.provider_documents || documentsData.provider_documents.length === 0) ? (
              <p style={{ color: "var(--text-secondary)", margin: 0 }}>No provider documents uploaded yet.</p>
            ) : (
              <div className="table-responsive">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Provider Business</th>
                      <th>Type</th>
                      <th>Doc Number</th>
                      <th>Uploaded</th>
                      <th>Status</th>
                      <th>File Link</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {documentsData.provider_documents.map((doc) => (
                      <tr key={doc.document_id}>
                        <td>#{doc.document_id}</td>
                        <td>
                          <strong>{doc.business_name || "Provider"}</strong>
                        </td>
                        <td><span style={{ fontWeight: 600 }}>{doc.document_type}</span></td>
                        <td>{doc.document_number || "—"}</td>
                        <td>{formatDate(doc.uploaded_at)}</td>
                        <td>
                          <span className={`status-badge ${getStatusBadgeClass(doc.status)}`}>
                            {doc.status}
                          </span>
                        </td>
                        <td>
                          <a
                            href={`${API_BASE}${doc.document_url}`}
                            target="_blank"
                            rel="noreferrer"
                            className="btn btn-outline btn-sm"
                            style={{ padding: "3px 8px", fontSize: 11 }}
                          >
                            View File ↗
                          </a>
                        </td>
                        <td>
                          {doc.status === "PENDING" ? (
                            <div style={{ display: "flex", gap: 6 }}>
                              <button
                                type="button"
                                onClick={() => handleReviewDoc("provider", doc.document_id, "VERIFIED")}
                                disabled={actionLoadingId === `provider-${doc.document_id}`}
                                className="btn btn-success btn-sm"
                                style={{ padding: "4px 8px", fontSize: 11 }}
                              >
                                ✓ Verify
                              </button>
                              <button
                                type="button"
                                onClick={() => setRejectionModal({ type: "provider", id: doc.document_id })}
                                disabled={actionLoadingId === `provider-${doc.document_id}`}
                                className="btn btn-danger btn-sm"
                                style={{ padding: "4px 8px", fontSize: 11 }}
                              >
                                ✕ Reject
                              </button>
                            </div>
                          ) : (
                            <span style={{ fontSize: 12, color: "var(--text-muted)" }}>
                              {doc.rejection_reason ? `Rejected: ${doc.rejection_reason}` : "Reviewed"}
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Rejection Modal */}
      {rejectionModal && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0,0,0,0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 9999,
          }}
        >
          <div className="container-card" style={{ maxWidth: 460, width: "90%", background: "#fff" }}>
            <h3 style={{ margin: "0 0 12px", color: "var(--coffee-bean)" }}>Reject Document #{rejectionModal.id}</h3>
            <p style={{ margin: "0 0 16px", fontSize: 13, color: "var(--text-secondary)" }}>
              Provide a reason for rejecting this document so the user can re-upload correctly:
            </p>
            <textarea
              className="form-control"
              rows={3}
              placeholder="e.g. Image is blurry, name mismatch, expired license..."
              value={rejectionReason}
              onChange={(e) => setRejectionReason(e.target.value)}
              style={{ width: "100%", marginBottom: 16 }}
            />
            <div style={{ display: "flex", gap: 10, justifyContent: "flex-end" }}>
              <button
                type="button"
                className="btn btn-outline btn-sm"
                onClick={() => {
                  setRejectionModal(null);
                  setRejectionReason("");
                }}
              >
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-danger btn-sm"
                onClick={() => handleReviewDoc(rejectionModal.type, rejectionModal.id, "REJECTED", rejectionReason)}
              >
                Confirm Rejection
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: PENDING PROVIDERS */}
      {activeTab === "providers" && (
        <div>
          {pendingProviders.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">✅</div>
              <h3>No pending providers</h3>
              <p>All registered logistics providers have been reviewed.</p>
            </div>
          ) : (
            <div className="container-cards">
              {pendingProviders.map((p) => (
                <div key={p.provider_id} className="container-card">
                  <div className="container-card-top">
                    <h3 style={{ margin: 0, fontSize: 16, color: "var(--coffee-bean)" }}>
                      {p.business_name}
                    </h3>
                    <span className="status-badge status-pending">Pending Approval</span>
                  </div>

                  <div className="container-card-stats">
                    <div className="container-stat">
                      <label>Email</label>
                      <p style={{ fontSize: 12 }}>{p.email}</p>
                    </div>
                    <div className="container-stat">
                      <label>Contact Phone</label>
                      <p>{p.contact}</p>
                    </div>
                  </div>

                  <div style={{ fontSize: 12, color: "var(--text-secondary)" }}>
                    <strong>Address:</strong> {p.business_address}
                  </div>

                  <div className="container-card-footer">
                    <button
                      type="button"
                      onClick={() => handleApprove(p.provider_id)}
                      disabled={actionLoadingId === p.provider_id}
                      className="btn btn-success btn-sm"
                      style={{ flex: 1 }}
                    >
                      {actionLoadingId === p.provider_id ? "..." : "✓ Approve"}
                    </button>
                    <button
                      type="button"
                      onClick={() => handleReject(p.provider_id)}
                      disabled={actionLoadingId === p.provider_id}
                      className="btn btn-danger btn-sm"
                      style={{ flex: 1 }}
                    >
                      {actionLoadingId === p.provider_id ? "..." : "✕ Reject"}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* TAB 3: ALL BOOKINGS */}
      {activeTab === "bookings" && (
        <div className="profile-card" style={{ maxWidth: "100%", overflowX: "auto" }}>
          {allBookings.length === 0 ? (
            <div className="empty-state">
              <h3>No platform bookings yet</h3>
            </div>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
              <thead>
                <tr style={{ borderBottom: "2px solid var(--border)", textAlign: "left" }}>
                  <th style={{ padding: "10px 12px" }}>ID</th>
                  <th style={{ padding: "10px 12px" }}>Route</th>
                  <th style={{ padding: "10px 12px" }}>Exporter</th>
                  <th style={{ padding: "10px 12px" }}>Provider</th>
                  <th style={{ padding: "10px 12px" }}>Capacity</th>
                  <th style={{ padding: "10px 12px" }}>Total Price</th>
                  <th style={{ padding: "10px 12px" }}>Status</th>
                  <th style={{ padding: "10px 12px" }}>Date</th>
                </tr>
              </thead>
              <tbody>
                {allBookings.map((b) => (
                  <tr key={b.booking_id} style={{ borderBottom: "1px solid var(--border)" }}>
                    <td style={{ padding: "12px" }}>#{b.booking_id}</td>
                    <td style={{ padding: "12px", fontWeight: 600 }}>
                      {b.origin} → {b.destination}
                    </td>
                    <td style={{ padding: "12px" }}>
                      <div>{b.exporter_name}</div>
                      <small style={{ color: "var(--text-muted)" }}>{b.exporter_email}</small>
                    </td>
                    <td style={{ padding: "12px" }}>{b.provider_business_name}</td>
                    <td style={{ padding: "12px" }}>{b.booked_capacity_kg.toLocaleString()} kg</td>
                    <td style={{ padding: "12px", fontWeight: 700, color: "var(--autumn-ember)" }}>
                      ₹{b.total_price.toFixed(2)}
                    </td>
                    <td style={{ padding: "12px" }}>
                      <span className={`status-badge ${getStatusBadgeClass(b.status)}`}>
                        {b.status}
                      </span>
                    </td>
                    <td style={{ padding: "12px", color: "var(--text-muted)" }}>
                      {formatDate(b.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
