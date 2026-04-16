from __future__ import annotations

import re
from urllib.parse import urlparse

from src.config import COMMON_SHORTENERS, PROTECTED_BRANDS, SUSPICIOUS_KEYWORDS


IPV4_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def _normalize_url(url: str) -> str:
    url = str(url).strip()
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        return f"http://{url}"
    return url


def _safe_parse(url: str):
    return urlparse(_normalize_url(url))


def _root_token(host: str) -> str:
    host = str(host or "").split(":")[0].lower().strip(".")
    if not host:
        return ""
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 2:
        return labels[-2]
    return labels[0]


def _levenshtein_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    previous_row = list(range(len(b) + 1))
    for i, char_a in enumerate(a, start=1):
        current_row = [i]
        for j, char_b in enumerate(b, start=1):
            insertions = previous_row[j] + 1
            deletions = current_row[j - 1] + 1
            substitutions = previous_row[j - 1] + (0 if char_a == char_b else 1)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def _brand_typo_score(host: str) -> tuple[int, float]:
    token = _root_token(host)
    if not token or len(token) < 4:
        return 0, 0.0

    best_similarity = 0.0
    looks_like_typo = 0
    for brand in PROTECTED_BRANDS:
        distance = _levenshtein_distance(token, brand)
        max_len = max(len(token), len(brand))
        similarity = 1.0 - (distance / max_len)
        if similarity > best_similarity:
            best_similarity = similarity

        # Flag close misspellings (e.g. facebool vs facebook) but exclude exact matches.
        if distance in {1, 2} and token != brand and abs(len(token) - len(brand)) <= 2:
            looks_like_typo = 1

    return looks_like_typo, round(best_similarity, 4)


def count_suspicious_keywords(url: str) -> int:
    lowered = _normalize_url(url).lower()
    return sum(1 for keyword in SUSPICIOUS_KEYWORDS if keyword in lowered)


def extract_url_features(url: str) -> dict[str, float]:
    normalized = _normalize_url(url)
    parsed = _safe_parse(normalized)
    host = parsed.netloc
    path = parsed.path or ""
    url_text = normalized

    digits = sum(character.isdigit() for character in url_text)
    special_chars = sum(not character.isalnum() and character not in {":", "/"} for character in url_text)
    dots = url_text.count(".")
    hyphens = url_text.count("-")
    slashes = url_text.count("/")
    query_string = 1 if parsed.query else 0
    subdomain_count = max(host.count(".") - 1, 0) if host else 0
    looks_like_brand_typo, brand_similarity_score = _brand_typo_score(host)

    lower_url = url_text.lower()
    features = {
        "url_length": len(url_text),
        "domain_length": len(host),
        "path_length": len(path),
        "num_dots": dots,
        "num_hyphens": hyphens,
        "num_slashes": slashes,
        "num_digits": digits,
        "num_special_chars": special_chars,
        "has_at_symbol": 1 if "@" in url_text else 0,
        "has_ip_address": 1 if IPV4_REGEX.search(host or url_text) else 0,
        "subdomain_count": subdomain_count,
        "uses_https": 1 if parsed.scheme.lower() == "https" else 0,
        "suspicious_keyword_count": count_suspicious_keywords(url_text),
        "has_login_keyword": 1 if "login" in lower_url else 0,
        "has_verify_keyword": 1 if "verify" in lower_url else 0,
        "has_secure_keyword": 1 if "secure" in lower_url else 0,
        "has_update_keyword": 1 if "update" in lower_url else 0,
        "has_bank_keyword": 1 if "bank" in lower_url else 0,
        "has_account_keyword": 1 if "account" in lower_url else 0,
        "has_confirm_keyword": 1 if "confirm" in lower_url else 0,
        "has_password_keyword": 1 if "password" in lower_url else 0,
        "has_signin_keyword": 1 if "signin" in lower_url or "sign-in" in lower_url else 0,
        "has_query_string": query_string,
        "is_shortened_like": 1 if parsed.netloc.lower() in COMMON_SHORTENERS or len(path) <= 3 and len(host) <= 15 else 0,
        "looks_like_brand_typo": looks_like_brand_typo,
        "brand_similarity_score": brand_similarity_score,
    }
    return features
