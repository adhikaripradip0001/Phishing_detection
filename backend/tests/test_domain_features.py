from src import domain_features


def test_domain_features_graceful_failure(monkeypatch) -> None:
    monkeypatch.setattr(domain_features, "whois", None)
    features = domain_features.extract_domain_features("https://example.com")
    assert features["has_whois_info"] == 0
    assert features["domain_age_days"] == 0
