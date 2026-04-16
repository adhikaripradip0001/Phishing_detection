export default function Header() {
  return (
    <header className="header-shell">
      <div>
        <p className="eyebrow">Master's Dissertation Prototype</p>
        <h1>AI-Based Phishing Website Detection System</h1>
        <p className="header-copy">
          Hybrid URL, domain, and content feature engineering with supervised machine learning and live prediction.
        </p>
      </div>
      <div className="header-badge">
        <span>Binary Classification</span>
        <strong>Phishing vs Legitimate</strong>
      </div>
    </header>
  );
}
