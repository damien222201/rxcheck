"""
Thin client for openFDA's drug label API.

We deliberately do NOT compute or invent any interaction "severity" or
risk score here. We only fetch the actual FDA-approved label text and
surface it, clearly cited, so the person (and their pharmacist/doctor)
can read the real source rather than trust an automated judgment call.
"""
import requests

FDA_BASE = "https://api.fda.gov/drug/label.json"
REQUEST_TIMEOUT = 12

# Simple in-process cache so repeated lookups of the same drug within a
# run don't hit the API twice. Not persisted between requests/restarts.
_cache = {}


def search_drug_label(drug_name):
    """
    Look up a drug by brand, generic, or substance name. Returns a dict
    with the fields we care about, or None if nothing was found.
    """
    key = drug_name.strip().lower()
    if not key:
        return None
    if key in _cache:
        return _cache[key]

    query = (
        f'(openfda.generic_name:"{key}" OR openfda.brand_name:"{key}" '
        f'OR openfda.substance_name:"{key}")'
    )
    try:
        resp = requests.get(
            FDA_BASE, params={"search": query, "limit": 1},
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code == 404:
            _cache[key] = None
            return None
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            _cache[key] = None
            return None

        r = results[0]
        openfda = r.get("openfda", {})
        normalized = {
            "query": drug_name,
            "brand_names": openfda.get("brand_name", []),
            "generic_names": openfda.get("generic_name", []),
            "substance_names": openfda.get("substance_name", []),
            "drug_interactions": r.get("drug_interactions", []),
            "warnings": r.get("warnings", []) or r.get("warnings_and_cautions", []),
            "indications": r.get("indications_and_usage", []),
        }
        _cache[key] = normalized
        return normalized
    except Exception as e:
        print(f"[warn] openFDA lookup failed for '{drug_name}': {e}")
        return {"query": drug_name, "error": str(e)}


def all_names(drug_data):
    """Every name openFDA has on file for this drug, lowercased, for matching."""
    if not drug_data:
        return set()
    names = set()
    for field in ("brand_names", "generic_names", "substance_names"):
        for n in drug_data.get(field, []):
            names.add(n.strip().lower())
    names.add(drug_data.get("query", "").strip().lower())
    return names


def find_cross_mentions(target_drug_data, other_drug_data):
    """
    Check whether other_drug's names appear in target_drug's interaction/
    warnings text. Returns the matching excerpt sentences, or an empty list.
    Pure text matching against real label text — nothing inferred.
    """
    if not target_drug_data or not other_drug_data:
        return []

    other_names = all_names(other_drug_data)
    other_names = {n for n in other_names if n and len(n) > 2}  # skip tiny/empty tokens
    if not other_names:
        return []

    haystack_sections = (target_drug_data.get("drug_interactions", []) or []) + \
                         (target_drug_data.get("warnings", []) or [])

    matches = []
    for section in haystack_sections:
        lower_section = section.lower()
        if any(name in lower_section for name in other_names):
            matches.append(section)
    return matches
