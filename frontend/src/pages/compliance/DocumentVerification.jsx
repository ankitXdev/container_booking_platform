import { useState, useEffect } from "react";
import useAuth from "../../hooks/useAuth";
import {
  uploadExporterDocument,
  getMyExporterDocuments,
  getExporterComplianceStatus,
  uploadProviderDocument,
  getMyProviderDocuments,
  getProviderComplianceStatus,
} from "../../services/documentService";
import "../../assets/dashboard.css";

const API_BASE = "http://localhost:8000";

const EXPORTER_DOC_TYPES = [
  { value: "IEC", label: "IEC (Importer-Exporter Code)" },
  { value: "GST", label: "GSTIN Registration Certificate" },
  { value: "PAN", label: "Company / Business PAN Card" },
  { value: "BUSINESS_REG", label: "Business Registration / Incorporation" },
];

const PROVIDER_DOC_TYPES = [
  { value: "MTO_LICENSE", label: "MTO (Multimodal Transport Operator) License" },
  { value: "GST", label: "GSTIN Certificate" },
  { value: "PAN", label: "Business / Entity PAN Card" },
  { value: "FREIGHT_INSURANCE", label: "Cargo / Freight Liability Insurance" },
  { value: "CUSTOMS_BROKER", label: "Customs Broker License" },
];

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

const DocumentVerification = () => {
  const { user } = useAuth();
  const role = user?.role?.toLowerCase() || "exporter";
  const isProvider = role === "provider";

  const [compliance, setCompliance] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Upload Form State
  const [docType, setDocType] = useState(isProvider ? "MTO_LICENSE" : "IEC");
  const [docNumber, setDocNumber] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const fetchStatusAndDocs = async () => {
    setLoading(true);
    setError("");
    try {
      if (isProvider) {
        const [comp, docs] = await Promise.all([
          getProviderComplianceStatus(),
          getMyProviderDocuments(),
        ]);
        setCompliance(comp);
        setDocuments(docs);
      } else {
        const [comp, docs] = await Promise.all([
          getExporterComplianceStatus(),
          getMyExporterDocuments(),
        ]);
        setCompliance(comp);
        setDocuments(docs);
      }
    } catch (err) {
      setError(err.message || "Failed to load document records.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatusAndDocs();
  }, [isProvider]);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError("Please select a document file to upload (PDF, PNG, JPG).");
      return;
    }

    setUploading(true);
    setError("");
    setSuccess("");

    try {
      const payload = {
        document_type: docType,
        document_number: docNumber,
        file: selectedFile,
      };

      if (isProvider) {
        await uploadProviderDocument(payload);
      } else {
        await uploadExporterDocument(payload);
      }

      setSuccess("Document submitted successfully! Awaiting admin review.");
      setSelectedFile(null);
      setDocNumber("");
      // Reset file input element if needed
      const fileInput = document.getElementById("file-upload-input");
      if (fileInput) fileInput.value = "";

      await fetchStatusAndDocs();
    } catch (err) {
      setError(err.message || "Failed to upload document.");
    } finally {
      setUploading(false);
    }
  };

  const docTypesList = isProvider ? PROVIDER_DOC_TYPES : EXPORTER_DOC_TYPES;

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <span className="page-eyebrow">COMPLIANCE & KYC VERIFICATION</span>
        <h1>Account Documents & Verification</h1>
        <p>
          {isProvider
            ? "Upload your transport licenses and business tax registrations. Admin verification is required to publish containers and accept cargo bookings."
            : "Upload your business identity and Import-Export Code (IEC). Admin verification unlocks full container space booking privileges."}
        </p>
      </div>

      {error && <div className="feedback-error" style={{ marginBottom: 20 }}>{error}</div>}
      {success && <div className="feedback-success" style={{ marginBottom: 20 }}>{success}</div>}

      {/* Compliance Status Card */}
      <div
        className="container-card"
        style={{
          marginBottom: 32,
          borderLeft: `5px solid ${
            compliance?.is_verified
              ? "#059669"
              : compliance?.status === "PENDING"
              ? "#D97706"
              : "#DC2626"
          }`,
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 16 }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
              <span style={{ fontSize: 22 }}>
                {compliance?.is_verified ? "🛡️" : compliance?.status === "PENDING" ? "⏳" : "⚠️"}
              </span>
              <h3 style={{ margin: 0, fontSize: 18, color: "var(--coffee-bean)" }}>
                Verification Status:{" "}
                <span
                  className={
                    compliance?.is_verified
                      ? "status-badge status-approved"
                      : compliance?.status === "PENDING"
                      ? "status-badge status-pending"
                      : "status-badge status-rejected"
                  }
                >
                  {compliance?.status || "NOT SUBMITTED"}
                </span>
              </h3>
            </div>
            <p style={{ margin: 0, fontSize: 14, color: "var(--text-secondary)" }}>
              {compliance?.message || "Documents required to access full platform features."}
            </p>
          </div>
          <div>
            <span
              style={{
                fontSize: 13,
                fontWeight: 600,
                color: compliance?.is_verified ? "#059669" : "#D97706",
                background: compliance?.is_verified ? "#ECFDF5" : "#FFFBEB",
                padding: "8px 14px",
                borderRadius: 20,
                display: "inline-block",
              }}
            >
              {compliance?.is_verified ? "✓ Full Access Granted" : "🔒 Action Required"}
            </span>
          </div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: 24, marginBottom: 40 }}>
        {/* Upload Form Card */}
        <div className="container-card">
          <h2 style={{ fontSize: 18, margin: "0 0 16px", color: "var(--coffee-bean)" }}>
            📤 Upload Verification Document
          </h2>
          <form onSubmit={handleUploadSubmit}>
            <div className="form-group">
              <label htmlFor="doc-type">Document Type *</label>
              <select
                id="doc-type"
                className="form-control"
                value={docType}
                onChange={(e) => setDocType(e.target.value)}
                required
              >
                {docTypesList.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="doc-number">Document / Registration Number (Optional)</label>
              <input
                id="doc-number"
                type="text"
                className="form-control"
                placeholder="e.g. 05AAACB1234F1Z5 or IEC0123456789"
                value={docNumber}
                onChange={(e) => setDocNumber(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="file-upload-input">Document File (PDF, PNG, JPG - max 10MB) *</label>
              <input
                id="file-upload-input"
                type="file"
                className="form-control"
                accept=".pdf,.png,.jpg,.jpeg,.webp"
                onChange={handleFileChange}
                required
              />
              {selectedFile && (
                <span style={{ display: "block", fontSize: 12, color: "var(--text-secondary)", marginTop: 4 }}>
                  Selected: <strong>{selectedFile.name}</strong> ({(selectedFile.size / 1024).toFixed(1)} KB)
                </span>
              )}
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              disabled={uploading}
              style={{ width: "100%", marginTop: 8 }}
            >
              {uploading ? "Uploading Document..." : "Submit Document for Review"}
            </button>
          </form>
        </div>

        {/* Verification Info / Guidelines */}
        <div className="container-card" style={{ background: "var(--white)" }}>
          <h2 style={{ fontSize: 18, margin: "0 0 16px", color: "var(--coffee-bean)" }}>
            📋 Verification Guidelines
          </h2>
          <ul style={{ margin: 0, paddingLeft: 20, fontSize: 14, color: "var(--text-secondary)", lineHeight: 1.8 }}>
            <li>
              <strong>Exporters:</strong> Must provide an active Importer-Exporter Code (IEC) or valid GSTIN to unlock container space booking and payment gateways.
            </li>
            <li>
              <strong>Providers:</strong> Must hold valid shipping / freight forwarding licenses (MTO or Customs Brokerage) to create container space listings.
            </li>
            <li>
              Supported formats: <code>.pdf</code>, <code>.png</code>, <code>.jpg</code>.
            </li>
            <li>
              Ensure document details (names, registration numbers) are clearly legible.
            </li>
            <li>
              Admin reviews are typically processed within 24 business hours.
            </li>
          </ul>
        </div>
      </div>

      {/* Uploaded Documents List */}
      <div className="container-card">
        <h2 style={{ fontSize: 18, margin: "0 0 16px", color: "var(--coffee-bean)" }}>
          📂 Uploaded Documents History ({documents.length})
        </h2>

        {loading ? (
          <p style={{ color: "var(--text-secondary)" }}>Loading documents...</p>
        ) : documents.length === 0 ? (
          <div style={{ textAlign: "center", padding: "40px 20px" }}>
            <span style={{ fontSize: 40, display: "block", marginBottom: 12 }}>📁</span>
            <p style={{ color: "var(--text-secondary)", margin: "0 0 8px" }}>
              No compliance documents uploaded yet.
            </p>
            <span style={{ fontSize: 13, color: "var(--text-secondary)" }}>
              Use the upload form above to submit your verification files.
            </span>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Document No.</th>
                  <th>Uploaded Date</th>
                  <th>Status</th>
                  <th>Rejection Note</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.document_id}>
                    <td>
                      <strong>{doc.document_type}</strong>
                    </td>
                    <td>{doc.document_number || "—"}</td>
                    <td>{formatDate(doc.uploaded_at)}</td>
                    <td>
                      <span
                        className={
                          doc.status === "VERIFIED"
                            ? "status-badge status-approved"
                            : doc.status === "PENDING"
                            ? "status-badge status-pending"
                            : "status-badge status-rejected"
                        }
                      >
                        {doc.status}
                      </span>
                    </td>
                    <td style={{ color: doc.rejection_reason ? "#DC2626" : "var(--text-secondary)", maxWidth: 220 }}>
                      {doc.rejection_reason || "—"}
                    </td>
                    <td>
                      <a
                        href={`${API_BASE}${doc.document_url}`}
                        target="_blank"
                        rel="noreferrer"
                        className="btn btn-outline btn-sm"
                        style={{ padding: "4px 10px", fontSize: 12 }}
                      >
                        View File ↗
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentVerification;
