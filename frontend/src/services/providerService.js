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

const formatErrorMessage = (detail, fallback = "An error occurred") => {
  if (!detail) return fallback;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((d) => {
        const field = d.loc && d.loc.length > 1 ? `${d.loc[d.loc.length - 1]}: ` : "";
        return `${field}${d.msg || JSON.stringify(d)}`;
      })
      .join("; ");
  }
  if (typeof detail === "object") {
    return detail.msg || detail.message || JSON.stringify(detail);
  }
  return fallback;
};

/*
|--------------------------------------------------------------------------
| Register Provider
|--------------------------------------------------------------------------
| POST /providers/
|
| Used when a provider creates their provider profile.
|--------------------------------------------------------------------------
*/

export const registerProvider = async ({
  business_name,
  business_address,
  contact,
}) => {
  const response = await fetch(`${API_URL}/providers/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      business_name,
      business_address,
      contact,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      formatErrorMessage(data.detail, "Failed to register provider")
    );
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Search Providers
|--------------------------------------------------------------------------
| GET /providers/?business_name=...
|
| Searches approved providers by business name.
|--------------------------------------------------------------------------
*/

export const searchProviders = async (businessName) => {
  const response = await fetch(
    `${API_URL}/providers/?business_name=${encodeURIComponent(
      businessName
    )}`,
    {
      method: "GET",
      headers: getAuthHeaders(),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      formatErrorMessage(data.detail, "Failed to search providers")
    );
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Update Provider
|--------------------------------------------------------------------------
| PUT /providers/{provider_id}
|
| Updates the provider's business information.
|--------------------------------------------------------------------------
*/

export const updateProvider = async (
  providerId,
  {
    business_name,
    business_address,
    contact,
  }
) => {
  const response = await fetch(
    `${API_URL}/providers/${providerId}`,
    {
      method: "PUT",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        business_name,
        business_address,
        contact,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      formatErrorMessage(data.detail, "Failed to update provider")
    );
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Get Provider Details
|--------------------------------------------------------------------------
| GET /providers/{provider_id}
|
| Returns details of an approved provider.
|--------------------------------------------------------------------------
*/

export const getProviderDetails = async (providerId) => {
  const response = await fetch(
    `${API_URL}/providers/${providerId}`,
    {
      method: "GET",
      headers: getAuthHeaders(),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      formatErrorMessage(data.detail, "Failed to fetch provider details")
    );
  }

  return data;
};