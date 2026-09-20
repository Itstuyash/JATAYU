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
