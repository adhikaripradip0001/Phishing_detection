from __future__ import annotations

from urllib.parse import parse_qs, urlparse


def _normalize_url(url: str) -> str:
    value = str(url).strip()
    if not value.startswith(("http://", "https://")):
        value = f"http://{value}"
    return value


def _to_risk_ternary(value: float, low: float, high: float) -> int:
    if value <= low:
        return -1
    if value >= high:
        return 1
    return 0


def build_legacy_feature_mapping(url: str, base_features: dict[str, float]) -> dict[str, float]:
    normalized = _normalize_url(url)
    parsed = urlparse(normalized)
    query_components = parse_qs(parsed.query, keep_blank_values=True)

    num_external = float(base_features.get("num_external_links", 0))
    num_internal = float(base_features.get("num_internal_links", 0))
    total_links = num_external + num_internal
    pct_ext_links = (num_external / total_links) if total_links > 0 else 0.0

    path_segments = [segment for segment in parsed.path.split("/") if segment]
    query_length = float(len(parsed.query or ""))
    num_query_components = float(len(query_components))

    suspicious_words = float(base_features.get("suspicious_keyword_count", 0))
    js_redirect = float(base_features.get("has_js_redirect", 0))
    num_scripts = float(base_features.get("num_scripts", 0))
    uses_https = float(base_features.get("uses_https", 0))
    num_forms = float(base_features.get("num_forms", 0))
    suspicious_form_action = float(base_features.get("suspicious_form_action", 0))
    mailto_usage = float(base_features.get("mailto_usage", 0))
    has_iframe = float(base_features.get("has_iframe", 0))
    favicon_exists = float(base_features.get("favicon_exists", 0))

    frequent_mismatch = 1.0 if base_features.get("has_ip_address", 0) or suspicious_words >= 3 else 0.0
    insecure_forms = 1.0 if (uses_https == 0 and num_forms > 0) or suspicious_form_action > 0 else 0.0
    ext_meta_script_link_rt = float(
        _to_risk_ternary((pct_ext_links * 100.0) + min(num_scripts, 10.0), low=15.0, high=55.0)
    )
    ext_null_redirect_rt = float(_to_risk_ternary(js_redirect, low=0.0, high=1.0))

    return {
        "PctExtHyperlinks": pct_ext_links,
        "PctExtNullSelfRedirectHyperlinksRT": ext_null_redirect_rt,
        "FrequentDomainNameMismatch": frequent_mismatch,
        "PctExtResourceUrls": pct_ext_links,
        "PctNullSelfRedirectHyperlinks": js_redirect,
        "NumDash": float(base_features.get("num_hyphens", 0)),
        "NumNumericChars": float(base_features.get("num_digits", 0)),
        "ExtMetaScriptLinkRT": ext_meta_script_link_rt,
        "InsecureForms": insecure_forms,
        "SubmitInfoToEmail": mailto_usage,
        "PathLevel": float(len(path_segments)),
        "NumDots": float(base_features.get("num_dots", 0)),
        "PathLength": float(base_features.get("path_length", 0)),
        "NumSensitiveWords": suspicious_words,
        "UrlLength": float(base_features.get("url_length", 0)),
        "QueryLength": query_length,
        "IframeOrFrame": has_iframe,
        "HostnameLength": float(base_features.get("domain_length", 0)),
        "NumQueryComponents": num_query_components,
        "ExtFavicon": 0.0 if favicon_exists > 0 else 1.0,
    }


def adapt_features_for_selected_schema(
    url: str,
    base_features: dict[str, float],
    selected_features: list[str] | tuple[str, ...],
) -> dict[str, float]:
    selected_set = set(selected_features)
    if not selected_set:
        return base_features

    missing = [feature for feature in selected_features if feature not in base_features]
    if not missing:
        return base_features

    legacy_mapped = build_legacy_feature_mapping(url, base_features)
    merged = dict(base_features)
    for name, value in legacy_mapped.items():
        if name in selected_set:
            merged[name] = value
    return merged
