import { useState } from "react";
import { requestPrediction } from "../services/predictionService";

const fields = [
  { key: "BILL_AMT1", label: "Current month bill amount", group: "Current month", min: 0 },
  { key: "PAY_AMT1", label: "Current month payment amount", group: "Current month", min: 0 },
];

const initialValues = Object.fromEntries(fields.map(({ key }) => [key, ""]));

export default function PredictionForm({ onPrediction }) {
  const [values, setValues] = useState(initialValues);
  const [customerId, setCustomerId] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function updateValue(event) {
    setValues((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function submit(event) {
    event.preventDefault();
    if (!customerId.trim() || Object.values(values).some((value) => value === "")) {
      setError("Enter a customer ID and both current-month values.");
      return;
    }

    setError("");
    setLoading(true);
    try {
      const numericValues = Object.fromEntries(
        Object.entries(values).map(([key, value]) => [key, Number(value)]),
      );
      onPrediction(await requestPrediction({
        ...numericValues,
        customer_id: Number(customerId),
      }));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="assessment-card" onSubmit={submit}>
      {error && <p className="form-error">{error}</p>}
      <div className="customer-entry">
        <label>
          Customer ID
          <input
            name="customer_id"
            type="number"
            min="1"
            placeholder="1"
            value={customerId}
            onChange={(event) => setCustomerId(event.target.value)}
            required
          />
        </label>
        <p>The ID is matched against the imported UCI customer table.</p>
      </div>
      {["Current month"].map((group) => (
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
