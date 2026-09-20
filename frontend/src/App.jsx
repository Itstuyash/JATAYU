import { useState } from "react";
import AssessmentPage from "./pages/AssessmentPage";

export default function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app-shell">
      <aside>
        <a className="brand" href="#top">JATAYU</a>
        <p>Credit Risk Intelligence</p>
        <nav><a className="active" href="#assessment">New assessment</a></nav>
        <small>Connected to Flask API</small>
      </aside>
      <div className="content" id="top">
        <header><span>Underwriting workspace</span><span className="status">● API-backed</span></header>
        <AssessmentPage result={result} onPrediction={setResult} />
      </div>
    </div>
  );
}
