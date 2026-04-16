export default function FeatureList({ features }) {
  if (!features) {
    return null;
  }

  const entries = Object.entries(features);

  return (
    <section className="card feature-card">
      <div className="section-title">
        <p className="eyebrow">Key Features</p>
        <h3>Extracted Feature Summary</h3>
      </div>
      <div className="feature-list">
        {entries.map(([key, value]) => (
          <div className="feature-item" key={key}>
            <span>{key.replace(/_/g, ' ')}</span>
            <strong>{String(value)}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
