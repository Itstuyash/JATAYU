import { useState } from "react";

const fields = [
  { key: "LIMIT_BAL", label: "Credit limit", group: "Customer profile", min: 0 },
  { key: "AGE", label: "Age", group: "Customer profile", min: 0 },
  { key: "PAY_0", label: "Most recent repayment status (PAY_0)", group: "Customer profile" },
  ...[1, 2, 3, 4, 5, 6].map((month) => ({
    key: `BILL_AMT${month}`,
    label: `Bill amount — month ${month}`,
    group: "Six-month bill statements",
  })),
  ...[1, 2, 3, 4, 5, 6].map((month) => ({
    key: `PAY_AMT${month}`,
    label: `Payment amount — month ${month}`,
    group: "Six-month payments",
  })),
];

const initialValues = Object.fromEntries(fields.map(({ key }) => [key, ""]));

export default function PredictionForm({ onPrediction }) {
  const [values, setValues] = useState(initialValues);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function updateValue(event) {
    setValues((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function submit(event) {
    event.preventDefault();
    if (Object.values(values).some((value) => value === "")) {
      setError("Enter a value for every model input before requesting a prediction.");
      return;
    }

    setError("");
    setLoading(true);
    try {
      const numericValues = Object.fromEntries(
        Object.entries(values).map(([key, value]) => [key, Number(value)]),
      );
      const { requestPrediction } = await import("../services/predictionService");
      onPrediction(await requestPrediction(numericValues));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="assessment-card" onSubmit={submit}>
      {error && <p className="form-error">{error}</p>}
      {["Customer profile", "Six-month bill statements", "Six-month payments"].map((group) => (
        <fieldset key={group}>
          <legend>{group}</legend>
          <div className="field-grid">
            {fields.filter((field) => field.group === group).map((field) => (
              <label key={field.key}>
                {field.label}
                <input
                  name={field.key}
                  type="number"
                  step="any"
                  min={field.min}
                  value={values[field.key]}
                  onChange={updateValue}
                  required
                />
              </label>
            ))}
          </div>
        </fieldset>
      ))}
      <div className="form-actions">
        <button type="button" className="secondary" onClick={() => setValues(initialValues)}>
          Clear inputs
        </button>
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing risk…" : "Predict default risk"}
        </button>
      </div>
    </form>
  );
}
