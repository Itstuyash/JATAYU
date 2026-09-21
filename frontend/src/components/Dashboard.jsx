import { useEffect, useState } from "react";
import { fetchCustomerHistory, fetchDashboard } from "../services/predictionService";

function formatDate(value) {
  return new Date(value).toLocaleString();
}

function PredictionTable({ predictions }) {
  if (!predictions.length) return <p className="empty-state">No predictions have been stored yet.</p>;
  return <div className="table-wrap"><table>
    <thead><tr><th>Customer</th><th>Result</th><th>Probability</th><th>Model</th><th>Time</th></tr></thead>
    <tbody>{predictions.map((record) => <tr key={record.prediction_id}>
      <td>{record.customer_code}</td>
      <td><span className={`table-status ${record.prediction ? "risk" : "safe"}`}>{record.prediction_label}</span></td>
      <td>{(record.default_probability * 100).toFixed(1)}%</td>
      <td>{record.selected_model}</td>
      <td>{formatDate(record.created_at)}</td>
    </tr>)}</tbody>
  </table></div>;
}

export default function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [customerCode, setCustomerCode] = useState("");
  const [history, setHistory] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDashboard().then(setDashboard).catch((requestError) => setError(requestError.message));
  }, []);

  async function lookup(event) {
    event.preventDefault();
    if (!customerCode.trim()) return;
    setError("");
    try {
      setHistory((await fetchCustomerHistory(customerCode)).customer);
    } catch (requestError) {
      setHistory(null);
      setError(requestError.message);
    }
  }

  if (!dashboard && !error) return <main><p>Loading dashboard...</p></main>;
  const stats = dashboard?.stats;
  return <main>
    <section className="hero"><p className="eyebrow">JATAYU · Portfolio overview</p><h1>Risk operations dashboard</h1><p>Monitor stored assessments and trace a customer&apos;s prediction history.</p></section>
    {error && <p className="form-error">{error}</p>}
    {stats && <section className="stats-grid">
      <div><span>Total customers</span><strong>{stats.total_customers}</strong></div>
      <div><span>Total predictions</span><strong>{stats.total_predictions}</strong></div>
      <div><span>Predictions today</span><strong>{stats.predictions_today}</strong></div>
      <div><span>Default-risk rate</span><strong>{(stats.default_rate * 100).toFixed(1)}%</strong><small>{stats.default_predictions} defaults</small></div>
      <div><span>Best model selected</span><strong className="model-stat">{stats.best_model || "-"}</strong></div>
    </section>}
    <section className="dashboard-section"><div className="section-heading"><div><p className="eyebrow">Activity</p><h2>Recent five predictions</h2></div></div><PredictionTable predictions={dashboard?.recent_predictions || []} /></section>
    <section className="dashboard-section"><div className="section-heading"><div><p className="eyebrow">Customer lookup</p><h2>Prediction history</h2></div></div>
      <form className="lookup-form" onSubmit={lookup}><input value={customerCode} onChange={(event) => setCustomerCode(event.target.value)} placeholder="CUST-000001" aria-label="Customer ID" /><button type="submit">Find customer</button></form>
      {history && <><p className="history-meta"><strong>{history.customer_code}</strong> · created {formatDate(history.created_at)}</p><PredictionTable predictions={history.predictions} /></>}
    </section>
  </main>;
}