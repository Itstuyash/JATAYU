import PredictionForm from "../components/PredictionForm";
import PredictionResult from "../components/PredictionResult";

export default function AssessmentPage({ result, onPrediction }) {
  return (
    <main>
      <section className="hero">
        <p className="eyebrow">JATAYU · Risk intelligence</p>
        <h1>Credit card default assessment</h1>
        <p>Submit six months of customer account activity for a real-time default-risk prediction.</p>
      </section>
      <PredictionResult result={result} />
      <PredictionForm onPrediction={onPrediction} />
    </main>
  );
}
