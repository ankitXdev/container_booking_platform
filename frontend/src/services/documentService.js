const API_URL = import.meta.env.VITE_API_URL;

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");
  return {
    Authorization: `Bearer ${token}`,
  };
};

/*
|--------------------------------------------------------------------------
| EXPORTER DOCUMENTS API
|--------------------------------------------------------------------------
*/

export const uploadExporterDocument = async ({ document_type, document_number, file }) => {
  const formData = new FormData();
  formData.append("document_type", document_type);
  if (document_number) {
    formData.append("document_number", document_number);
  }
  formData.append("file", file);

  const response = await fetch(`${API_URL}/documents/exporter/upload`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: formData,
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to upload exporter document");
  }
  return data;
};

export const getMyExporterDocuments = async () => {
  const response = await fetch(`${API_URL}/documents/exporter/me`, {
    method: "GET",
    headers: {
      ...getAuthHeaders(),
      "Content-Type": "application/json",
    },
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch exporter documents");
  }
  return data;
};

export const getExporterComplianceStatus = async () => {
  const response = await fetch(`${API_URL}/documents/exporter/status`, {
    method: "GET",
    headers: {
      ...getAuthHeaders(),
      "Content-Type": "application/json",
    },
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch compliance status");
  }
  return data;
};

/*
|--------------------------------------------------------------------------
| PROVIDER DOCUMENTS API
|--------------------------------------------------------------------------
*/

export const uploadProviderDocument = async ({ document_type, document_number, file }) => {
  const formData = new FormData();
  formData.append("document_type", document_type);
  if (document_number) {
    formData.append("document_number", document_number);
  }
  formData.append("file", file);

  const response = await fetch(`${API_URL}/documents/provider/upload`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: formData,
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to upload provider document");
  }
  return data;
};

export const getMyProviderDocuments = async () => {
  const response = await fetch(`${API_URL}/documents/provider/me`, {
    method: "GET",
    headers: {
      ...getAuthHeaders(),
      "Content-Type": "application/json",
    },
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch provider documents");
  }
  return data;
};

export const getProviderComplianceStatus = async () => {
  const response = await fetch(`${API_URL}/documents/provider/status`, {
    method: "GET",
    headers: {
      ...getAuthHeaders(),
      "Content-Type": "application/json",
    },
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch compliance status");
  }
  return data;
};

/*
|--------------------------------------------------------------------------
| ADMIN REVIEW API
|--------------------------------------------------------------------------
*/

export const getAllDocumentsForAdmin = async () => {
  const response = await fetch(`${API_URL}/admin/documents`, {
    method: "GET",
    headers: {
      ...getAuthHeaders(),
      "Content-Type": "application/json",
    },
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch documents for review");
  }
  return data;
};

export const reviewExporterDocument = async (documentId, { status, rejection_reason }) => {
  const response = await fetch(`${API_URL}/admin/documents/exporter/${documentId}/review`, {
    method: "PATCH",
    headers: {
      ...getAuthHeaders(),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      status,
      rejection_reason: rejection_reason || null,
    }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to review exporter document");
  }
  return data;
};

export const reviewProviderDocument = async (documentId, { status, rejection_reason }) => {
  const response = await fetch(`${API_URL}/admin/documents/provider/${documentId}/review`, {
    method: "PATCH",
    headers: {
      ...getAuthHeaders(),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      status,
      rejection_reason: rejection_reason || null,
    }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Failed to review provider document");
  }
  return data;
};
