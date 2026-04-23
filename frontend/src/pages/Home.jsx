import { useState } from 'react';

import ErrorMessage from '../components/ErrorMessage';
import FeatureList from '../components/FeatureList';
import Loader from '../components/Loader';
import ResultCard from '../components/ResultCard';
import UrlForm from '../components/UrlForm';
import { predictUrl } from '../services/api';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handlePredict = async (url, includeContent) => {
    if (!url) {
      setError('Please enter a valid URL.');
      return;
    }

    try {
      setError('');
      setLoading(true);
      const data = await predictUrl(url, includeContent);
      setResult(data);
    } catch (requestError) {
      const responseMessage = requestError?.response?.data?.error;
      setError(responseMessage || 'Prediction request failed. Check the backend API and try again.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <div className="content-shell">
        <header className="app-topbar card">
          <div className="topbar-left">
            <p className="topbar-kicker">Security Intelligence Platform</p>
            <h1>Phishing website detection</h1>
          </div>

          <div className="topbar-right">
            <span className="topbar-chip status-live">API Live</span>
          </div>
        </header>

        <UrlForm onSubmit={handlePredict} loading={loading} />
        <ErrorMessage message={error} />
        {loading && <Loader />}
        {result && <ResultCard result={result} />}
        {result && <FeatureList features={result.key_features} />}
      </div>
    </main>
  );
}
