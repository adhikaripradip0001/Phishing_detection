from src.url_features import extract_url_features


def test_url_feature_extraction_detects_suspicious_pattern() -> None:
    features = extract_url_features("http://secure-login.example-check.com/verify")
    assert features["has_login_keyword"] == 1
    assert features["has_verify_keyword"] == 1
    assert features["uses_https"] == 0
    assert features["url_length"] > 0


def test_url_feature_extraction_counts_new_suspicious_terms() -> None:
    features = extract_url_features("http://account-otp-security.example.com/reset")
    assert features["suspicious_keyword_count"] >= 3


def test_url_feature_extraction_counts_common_lure_terms() -> None:
    features = extract_url_features("http://winner-prize-claim-example.com/free-bonus")
    assert features["suspicious_keyword_count"] >= 4


def test_url_feature_extraction_detects_brand_typosquat() -> None:
    features = extract_url_features("https://facebool.com")
    assert features["looks_like_brand_typo"] == 1
    assert features["brand_similarity_score"] >= 0.75


def test_url_feature_extraction_detects_payment_brand_typosquat() -> None:
    features = extract_url_features("https://paytn.com")
    assert features["looks_like_brand_typo"] == 1
