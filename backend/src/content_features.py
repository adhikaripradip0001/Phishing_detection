from __future__ import annotations

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from src.config import CONTENT_REQUEST_TIMEOUT, SCRAPING_FAILURE_LOG_FILE, SUSPICIOUS_KEYWORDS
from src.utils import setup_logger


LOGGER = setup_logger("scraping_failures", SCRAPING_FAILURE_LOG_FILE)


def _normalize_url(url: str) -> str:
    url = str(url).strip()
    if not url.startswith(("http://", "https://")):
        return f"http://{url}"
    return url


def fetch_html(url: str, timeout: int = CONTENT_REQUEST_TIMEOUT) -> str | None:
    try:
        response = requests.get(
            _normalize_url(url),
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 PhishingDetectionResearch/1.0"},
        )
        response.raise_for_status()
        content_type = response.headers.get("content-type", "").lower()
        if "html" not in content_type and "xml" not in content_type and not response.text.lstrip().startswith("<"):
            return None
        return response.text
    except Exception as exc:  # pragma: no cover - network failures are normal in offline runs
        LOGGER.warning("scrape failed for %s: %s", url, exc)
        return None


def _is_internal_link(link: str, base_url: str) -> bool:
    if not link:
        return False
    parsed_link = urlparse(link)
    if not parsed_link.netloc:
        return True
    base_netloc = urlparse(base_url).netloc
    return parsed_link.netloc == base_netloc


def extract_content_features(url: str, html: str | None = None, enable_fetch: bool = True) -> dict[str, float]:
    page = html if html is not None else (fetch_html(url) if enable_fetch else None)
    features = {
        "num_forms": 0,
        "num_input_fields": 0,
        "has_password_field": 0,
        "num_external_links": 0,
        "num_internal_links": 0,
        "has_iframe": 0,
        "has_js_redirect": 0,
        "num_scripts": 0,
        "title_exists": 0,
        "favicon_exists": 0,
        "suspicious_form_action": 0,
        "empty_form_action": 0,
        "mailto_usage": 0,
    }

    if not page:
        return features

    soup = BeautifulSoup(page, "html.parser")
    forms = soup.find_all("form")
    links = soup.find_all("a", href=True)
    scripts = soup.find_all("script")
    base_url = _normalize_url(url)

    external = 0
    internal = 0
    for link in links:
        href = link.get("href", "")
        if href.startswith("mailto:"):
            features["mailto_usage"] = 1
        if _is_internal_link(urljoin(base_url, href), base_url):
            internal += 1
        else:
            external += 1

    suspicious_actions = 0
    empty_actions = 0
    password_fields = 0
    input_fields = 0
    for form in forms:
        action = str(form.get("action", "")).strip().lower()
        if not action or action in {"#", "javascript:void(0)"}:
            empty_actions += 1
        if action.startswith("mailto:"):
            features["mailto_usage"] = 1
        if any(keyword in action for keyword in SUSPICIOUS_KEYWORDS):
            suspicious_actions += 1

        inputs = form.find_all("input")
        input_fields += len(inputs)
        password_fields += sum(1 for input_tag in inputs if str(input_tag.get("type", "")).lower() == "password")

    lower_page = page.lower()
    js_redirect = 1 if any(token in lower_page for token in ["window.location", "location.href", "location.replace", "meta http-equiv=\"refresh\""]) else 0
    favicon_exists = 0
    for link in soup.find_all("link", rel=True):
        rel_value = link.get("rel", [])
        if isinstance(rel_value, (list, tuple)):
            rel_text = " ".join(str(item) for item in rel_value).lower()
        else:
            rel_text = str(rel_value).lower()
        if "icon" in rel_text:
            favicon_exists = 1
            break

    features.update(
        {
            "num_forms": len(forms),
            "num_input_fields": input_fields,
            "has_password_field": 1 if password_fields > 0 else 0,
            "num_external_links": external,
            "num_internal_links": internal,
            "has_iframe": 1 if soup.find("iframe") else 0,
            "has_js_redirect": js_redirect,
            "num_scripts": len(scripts),
            "title_exists": 1 if soup.title and soup.title.get_text(strip=True) else 0,
            "favicon_exists": favicon_exists,
            "suspicious_form_action": 1 if suspicious_actions > 0 else 0,
            "empty_form_action": 1 if empty_actions > 0 else 0,
            "mailto_usage": features["mailto_usage"],
        }
    )
    return features
