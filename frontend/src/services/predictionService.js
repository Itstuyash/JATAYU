export async function requestPrediction(formValues) {
  const response = await fetch("/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formValues),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Prediction request failed.");
  }
  return data;
}

export async function fetchDashboard() {
  const response = await fetch("/api/dashboard");
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Dashboard request failed.");
  return data;
}

export async function fetchCustomerHistory(customerCode) {
  const response = await fetch(`/api/customers/${encodeURIComponent(customerCode.trim())}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Customer lookup failed.");
  return data;
}
