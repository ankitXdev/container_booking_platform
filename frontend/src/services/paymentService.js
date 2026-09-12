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
| Create Payment Order
|--------------------------------------------------------------------------
| POST /payments/create-order
|
| Initiates a Razorpay order for a booking.
|--------------------------------------------------------------------------
*/
export const createPaymentOrder = async (bookingId) => {
  const response = await fetch(`${API_URL}/payments/create-order`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({ booking_id: Number(bookingId) }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to create payment order");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Verify Payment
|--------------------------------------------------------------------------
| POST /payments/verify
|
| Verifies Razorpay HMAC signature and confirms booking.
|--------------------------------------------------------------------------
*/
export const verifyPayment = async ({
  razorpay_order_id,
  razorpay_payment_id,
  razorpay_signature,
}) => {
  const response = await fetch(`${API_URL}/payments/verify`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      razorpay_order_id,
      razorpay_payment_id,
      razorpay_signature,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Payment verification failed");
  }

  return data;
};

/*
|--------------------------------------------------------------------------
| Get Payment Details
|--------------------------------------------------------------------------
| GET /payments/{booking_id}
|
| Retrieves payment transaction details & receipt for a booking.
|--------------------------------------------------------------------------
*/
export const getPaymentDetails = async (bookingId) => {
  const response = await fetch(`${API_URL}/payments/${bookingId}`, {
    method: "GET",
    headers: getAuthHeaders(),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to fetch payment details");
  }

  return data;
};
