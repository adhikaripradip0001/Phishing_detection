from __future__ import annotations

import os
from datetime import datetime, timezone
from urllib.parse import urlparse

import pandas as pd

from src.config import WHOIS_FAILURE_LOG_FILE
from src.utils import setup_logger

try:
    import tldextract

    TLD_EXTRACTOR = tldextract.TLDExtract(suffix_list_urls=None)
except Exception:  # pragma: no cover - fallback only
    tldextract = None
    TLD_EXTRACTOR = None

try:
    import whois
except Exception:  # pragma: no cover - fallback only
    whois = None


LOGGER = setup_logger("whois_failures", WHOIS_FAILURE_LOG_FILE)
SKIP_WHOIS = os.getenv("PHISHING_SKIP_WHOIS", "0").strip().lower() in {"1", "true", "yes", "on"}


def _normalize_url(url: str) -> str:
    url = str(url).strip()
    if not url.startswith(("http://", "https://")):
        return f"http://{url}"
    return url


def _extract_domain(url: str) -> str:
    parsed = urlparse(_normalize_url(url))
    host = parsed.netloc.split(":")[0]
    if TLD_EXTRACTOR is not None:
        extracted = TLD_EXTRACTOR(host)
        if extracted.domain and extracted.suffix:
            return f"{extracted.domain}.{extracted.suffix}"
    return host


def _first_date(value) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, list):
        value = next((item for item in value if item is not None), None)
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()
    if isinstance(value, datetime):
        return value
    return None


def _days_between(start: datetime | None, end: datetime | None) -> float:
    if not start or not end:
        return 0.0
    start_aware = start if start.tzinfo else start.replace(tzinfo=timezone.utc)
    end_aware = end if end.tzinfo else end.replace(tzinfo=timezone.utc)
    return max((end_aware - start_aware).days, 0)


def extract_domain_features(url: str) -> dict[str, float]:
    domain = _extract_domain(url)
    now = datetime.now(timezone.utc)
    features: dict[str, float] = {
        "has_whois_info": 0,
        "registrar_available": 0,
        "creation_date_exists": 0,
        "expiration_date_exists": 0,
        "domain_age_days": 0.0,
        "domain_expiry_days": 0.0,
        "registration_length_days": 0.0,
    }

    if not domain:
        return features

    if whois is None:
        LOGGER.warning("whois package unavailable for domain=%s", domain)
        return features

    if SKIP_WHOIS:
        return features

    try:
        record = whois.whois(domain)
        if not record:
            return features

        creation_date = _first_date(getattr(record, "creation_date", None))
        expiration_date = _first_date(getattr(record, "expiration_date", None))
        registrar = getattr(record, "registrar", None)

        features["has_whois_info"] = 1
        features["registrar_available"] = 1 if registrar else 0
        features["creation_date_exists"] = 1 if creation_date else 0
        features["expiration_date_exists"] = 1 if expiration_date else 0
        features["domain_age_days"] = float(_days_between(creation_date, now))
        features["domain_expiry_days"] = float(_days_between(now, expiration_date))
        features["registration_length_days"] = float(_days_between(creation_date, expiration_date))
        return features
    except Exception as exc:  # pragma: no cover - live lookup failures are expected
        LOGGER.warning("whois lookup failed for %s: %s", domain, exc)
        return features
