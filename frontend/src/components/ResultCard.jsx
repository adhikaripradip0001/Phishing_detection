export default function ResultCard({ result }) {
  if (!result) {
    return null;
  }

  const riskClass = result.predicted_label === 'phishing' ? 'danger' : 'safe';
  const percent = Math.round((result.phishing_probability || 0) * 100);

  return (
    <section className={`card result-card ${riskClass}`}>
      <div className="result-header">
        <div>
          <p className="eyebrow">Prediction Result</p>
          <h2>{result.predicted_label === 'phishing' ? 'Phishing Detected' : 'Legitimate Website'}</h2>
        </div>
        <div className="confidence-pill">{percent}% phishing probability</div>
      </div>

      <div className="result-meter">
        <div className="result-meter-fill" style={{ width: `${percent}%` }} />
      </div>

      <div className="result-grid">
        <div>
          <span>Entered URL</span>
          <strong className="url-value" title={result.url}>{result.url}</strong>
        </div>
        <div>
          <span>Confidence</span>
          <strong>{Math.round((result.confidence || 0) * 100)}%</strong>
        </div>
        <div>
          <span>Class Label</span>
          <strong>{result.class_label}</strong>
        </div>
      </div>

      <div className={`alert-box ${riskClass}`}>
        {result.warning}
      </div>
    </section>
  );
}
