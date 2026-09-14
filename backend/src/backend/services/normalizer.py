from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "fbclid", "ref", "source", "icid", "mc_cid", "mc_eid"
}


def normalize_url(url: str) -> str:
    """
    Normalizes a URL to prevent duplicate sources.
    - Standardizes scheme (http/https) to lowercase
    - Standardizes netloc to lowercase
    - Strips common tracking query parameters (utm_*, gclid, etc.)
    - Removes trailing slashes from path
    """
    if not url:
        return ""
        
    url = url.strip()
    parsed = urlparse(url)
    
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    
    # Strip trailing slash from path unless it's just '/'
    path = parsed.path
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
        
    # Clean query parameters
    query_params = parse_qs(parsed.query, keep_blank_values=False)
    filtered_params = {
        k: v for k, v in query_params.items()
        if k.lower() not in TRACKING_PARAMS
    }
    
    # Re-encode sorted params
    clean_query = urlencode(filtered_params, doseq=True)
    
    # Reconstruct clean URL
    normalized = urlunparse((
        scheme,
        netloc,
        path,
        parsed.params,
        clean_query,
        ""  # Strip fragment #section
    ))
    
    return normalized
