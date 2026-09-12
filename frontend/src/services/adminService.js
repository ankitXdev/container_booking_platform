const API_URL = "http://localhost:8000";

/*
|--------------------------------------------------------------------------
| Helper
|--------------------------------------------------------------------------
*/

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
};

/*
|--------------------------------------------------------------------------
| Get Pending Providers
|--------------------------------------------------------------------------
| GET /admin/providers/pending
|--------------------------------------------------------------------------
*/
export const getPendingProviders = async () => {
  const response = await fetch(`${API_URL}/admin/providers/pending`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch pending providers");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Approve Provider
|--------------------------------------------------------------------------
| PATCH /admin/providers/{provider_id}/approve
|--------------------------------------------------------------------------
*/
export const approveProvider = async (providerId) => {
  const response = await fetch(
    `${API_URL}/admin/providers/${providerId}/approve`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to approve provider");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Reject Provider
|--------------------------------------------------------------------------
| PATCH /admin/providers/{provider_id}/reject
|--------------------------------------------------------------------------
*/
export const rejectProvider = async (providerId) => {
  const response = await fetch(
    `${API_URL}/admin/providers/${providerId}/reject`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to reject provider");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Get Platform Stats
|--------------------------------------------------------------------------
| GET /admin/stats
|--------------------------------------------------------------------------
*/
export const getPlatformStats = async () => {
  const response = await fetch(`${API_URL}/admin/stats`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch platform stats");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Get All Platform Bookings
|--------------------------------------------------------------------------
| GET /admin/bookings
|--------------------------------------------------------------------------
*/
export const getAllBookings = async () => {
  const response = await fetch(`${API_URL}/admin/bookings`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch platform bookings");
  }

  return data;
};
