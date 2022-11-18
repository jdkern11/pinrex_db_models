def make_name_searchable(name: str) -> str:
    """Runs regex over the name to parse hard to match characters"""
    search_name = name.strip()
    search_name = name.lower()
    search_name = search_name.translate({ord(i): None for i in ":{}- ()[],‐'\""})
    return search_name
