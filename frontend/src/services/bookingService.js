const API_URL = import.meta.env.VITE_API_URL;

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
| Create Booking
|--------------------------------------------------------------------------
| POST /bookings/
|
| Exporter books capacity in a container.
|--------------------------------------------------------------------------
*/
export const createBooking = async ({ container_id, booked_capacity_kg }) => {
  const response = await fetch(`${API_URL}/bookings/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      container_id: Number(container_id),
      booked_capacity_kg: Number(booked_capacity_kg),
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to create booking");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| List Bookings
|--------------------------------------------------------------------------
| GET /bookings/
|
| Returns caller's bookings (exporter's bookings or provider's container bookings).
|--------------------------------------------------------------------------
*/
export const listBookings = async () => {
  const response = await fetch(`${API_URL}/bookings/`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch bookings");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Get Booking Details
|--------------------------------------------------------------------------
| GET /bookings/{booking_id}
|
| Exporter or owning provider only.
|--------------------------------------------------------------------------
*/
export const getBookingDetails = async (bookingId) => {
  const response = await fetch(`${API_URL}/bookings/${bookingId}`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch booking details");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Update Booking Status
|--------------------------------------------------------------------------
| PATCH /bookings/{booking_id}/status
|
| Provider only (confirmed | cancelled).
|--------------------------------------------------------------------------
*/
export const updateBookingStatus = async (bookingId, status) => {
  const response = await fetch(`${API_URL}/bookings/${bookingId}/status`, {
    method: "PATCH",
    headers: getAuthHeaders(),
    body: JSON.stringify({ status }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to update booking status");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Cancel Booking
|--------------------------------------------------------------------------
| POST /bookings/{booking_id}/cancel
|
| Exporter or owning provider. Restores container capacity.
|--------------------------------------------------------------------------
*/
export const cancelBooking = async (bookingId) => {
  const response = await fetch(`${API_URL}/bookings/${bookingId}/cancel`, {
    method: "POST",
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to cancel booking");
  }

  return data;
};
