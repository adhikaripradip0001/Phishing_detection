export default function Loader() {
  return (
    <div className="loader-shell" role="status" aria-live="polite">
      <div className="spinner" />
      <span>Processing URL and extracting features...</span>
    </div>
  );
}
