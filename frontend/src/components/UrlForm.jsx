import { useState } from 'react';

export default function UrlForm({ onSubmit, loading }) {
  const [url, setUrl] = useState('');
  const [includeContent, setIncludeContent] = useState(true);

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(url.trim(), includeContent);
  };

  return (
    <form className="card form-card" onSubmit={handleSubmit}>
      <label htmlFor="url-input">Enter website URL</label>
      <div className="input-row">
        <input
          id="url-input"
          type="url"
          placeholder="https://example.com"
          value={url}
          onChange={(event) => setUrl(event.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Detect'}
        </button>
      </div>
      <label className="toggle-row">
        <input
          type="checkbox"
          checked={includeContent}
          onChange={(event) => setIncludeContent(event.target.checked)}
        />
        <span>Include live content scraping when available</span>
      </label>
    </form>
  );
}
