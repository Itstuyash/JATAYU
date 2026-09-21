import { useState } from "react";
import AssessmentPage from "./pages/AssessmentPage";
import Dashboard from "./components/Dashboard";

export default function App() {
  const [result, setResult] = useState(null);
  const [view, setView] = useState(window.location.hash === "#dashboard" ? "dashboard" : "assessment");

  function changeView(nextView) {
    setView(nextView);
    window.history.replaceState(null, "", `#${nextView}`);
  }

  return (
    <div className="app-shell">
      <aside>
        <a className="brand" href="#top">JATAYU</a>
        <p>Credit Risk Intelligence</p>
        <nav><a className={view === "assessment" ? "active" : ""} href="#assessment" onClick={() => changeView("assessment")}>New assessment</a><a className={view === "dashboard" ? "active" : ""} href="#dashboard" onClick={() => changeView("dashboard")}>Dashboard</a></nav>
        <small>Connected to Flask API</small>
      </aside>
      <div className="content" id="top">
        <header><span>Underwriting workspace</span><span className="status">● API-backed</span></header>
        {view === "dashboard" ? <Dashboard /> : <AssessmentPage result={result} onPrediction={setResult} />}
      </div>
    </div>
  );
}
