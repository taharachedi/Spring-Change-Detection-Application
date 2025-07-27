import requests
import streamlit as st
from typing import Optional, Mapping, Any

@st.cache_data(ttl=3600)
def load_lottie_url(url: str) -> Optional[Mapping[str, Any]]:
    """
    Fetch and cache a Lottie animation JSON from the specified URL.

    Caches results for 1 hour to avoid re-fetching the same asset.

    Args:
        url: URL pointing to a Lottie JSON file.

    Returns:
         Parsed JSON as a dict if successful; None otherwise.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None