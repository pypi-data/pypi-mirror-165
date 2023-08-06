# we only support suffixes for now...todo expand functionality when we need to


def path_matches_pattern(filepath: str, pattern: str) -> bool:
    return filepath.endswith(pattern)
