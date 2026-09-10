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
| Create Container
|--------------------------------------------------------------------------
| POST /containers/
|
| Used by approved providers to create a new container listing.
|--------------------------------------------------------------------------
*/

export const createContainer = async ({
  origin,
  destination,
  departure_date,
  total_capacity_kg,
  available_capacity_kg,
  price_per_kg,
}) => {
  const response = await fetch(`${API_URL}/containers/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      origin,
      destination,
      departure_date,
      total_capacity_kg,
      available_capacity_kg,
      price_per_kg,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to create container listing");
  }

  return data;
};


/*
|--------------------------------------------------------------------------
| Search Containers
|--------------------------------------------------------------------------
| GET /containers/?origin=&destination=&min_capacity_kg=
|
| Public endpoint. Filters are all optional.
|--------------------------------------------------------------------------
*/

export const searchContainers = async ({
  origin = "",
  destination = "",
  min_capacity_kg = "",
} = {}) => {
  const params = new URLSearchParams();

  if (origin.trim()) params.append("origin", origin.trim());
  if (destination.trim()) params.append("destination", destination.trim());
  if (min_capacity_kg !== "" && min_capacity_kg !== null) {
    params.append("min_capacity_kg", min_capacity_kg);
  }

  const url = `${API_URL}/containers/${
    params.toString() ? `?${params.toString()}` : ""
  }`;

  const response = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to search containers");
  }

  return data;
};


/*
|--------------------------------------------------------------------------
| Get Container Details
|--------------------------------------------------------------------------
| GET /containers/{container_id}
|
| Public endpoint. Returns container info + provider business name/contact.
|--------------------------------------------------------------------------
*/

export const getContainerDetails = async (containerId) => {
  const response = await fetch(`${API_URL}/containers/${containerId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch container details");
  }

  return data;
};


/*
|--------------------------------------------------------------------------
| Update Container
|--------------------------------------------------------------------------
| PUT /containers/{container_id}
|
| Owning provider only.
|--------------------------------------------------------------------------
*/

export const updateContainer = async (
  containerId,
  {
    origin,
    destination,
    departure_date,
    total_capacity_kg,
    available_capacity_kg,
    price_per_kg,
  }
) => {
  const response = await fetch(`${API_URL}/containers/${containerId}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      origin,
      destination,
      departure_date,
      total_capacity_kg,
      available_capacity_kg,
      price_per_kg,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to update container");
  }

  return data;
};


/*
|--------------------------------------------------------------------------
| Delete Container
|--------------------------------------------------------------------------
| DELETE /containers/{container_id}
|
| Owning provider only.
|--------------------------------------------------------------------------
*/

export const deleteContainer = async (containerId) => {
  const response = await fetch(`${API_URL}/containers/${containerId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to delete container");
  }

  return data;
};


/*
|--------------------------------------------------------------------------
| Update Container Availability
|--------------------------------------------------------------------------
| PATCH /containers/{container_id}/availability
|
| Owning provider only. Toggles is_available.
|--------------------------------------------------------------------------
*/

export const updateContainerAvailability = async (containerId, is_available) => {
  const response = await fetch(
    `${API_URL}/containers/${containerId}/availability`,
    {
      method: "PATCH",
      headers: getAuthHeaders(),
      body: JSON.stringify({ is_available }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to update availability");
  }

  return data;
};
