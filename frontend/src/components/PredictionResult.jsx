function ModelCard({ model, primary }) {
  const probability = model.default_probability * 100;
  return <article className={`model-card ${primary ? "best-model" : ""} ${model.value ? "risk" : "safe"}`}>
    <div className="model-heading"><div>{primary && <p className="eyebrow">Best model · ROC-AUC {model.roc_auc.toFixed(4)}</p>}<h3>{model.name}</h3></div><span className="prediction-label">{model.label}</span></div>
    <div className="model-probability"><strong>{probability.toFixed(1)}%</strong><span>default probability</span></div>
    <div className="meter"><i style={{ width: `${probability}%` }} /></div>
    <div className="shap-section"><h4>Why this model predicted this result</h4><p>Positive values increase default risk; negative values reduce it.</p>
      {model.shap_explanation.slice(0, 4).map((driver) => <div className="shap-driver" key={driver.feature}><span>{driver.feature} ({Number(driver.value).toLocaleString()})</span><b className={driver.contribution >= 0 ? "positive" : "negative"}>{driver.contribution >= 0 ? "+" : ""}{driver.contribution.toFixed(3)}</b></div>)}
    </div>
  </article>;
}

export default function PredictionResult({ result }) {
  if (!result) return null;
  const best = result.models.find((model) => model.is_best_model);
  const others = result.models.filter((model) => !model.is_best_model);
  const { Total_bill, Total_pay, Outstanding } = result.features;
  return <section className="result-area" aria-live="polite">
    <div className="result-intro"><div><p className="eyebrow">Live model comparison · Prediction #{result.prediction_id}</p><h2>Default risk assessment</h2><p>The primary result uses the highest validation ROC-AUC model. The other predictions are shown for comparison.</p></div><span className="selection-chip">Selected by {result.selection_metric.toUpperCase()}</span></div>
    <ModelCard model={best} primary />
    <h3 className="comparison-title">Other trained models</h3>
    <div className="comparison-grid">{others.map((model) => <ModelCard key={model.name} model={model} />)}</div>
    <div className="financial-values"><div><span>Total bill</span><b>{Number(Total_bill).toLocaleString()}</b></div><div><span>Total payment</span><b>{Number(Total_pay).toLocaleString()}</b></div><div><span>Outstanding</span><b>{Number(Outstanding).toLocaleString()}</b></div></div>
  </section>;
}
