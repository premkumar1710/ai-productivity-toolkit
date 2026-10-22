"""
Sample buggy code file for automated debugging demonstrations.
Contains deliberate bugs: ZeroDivisionError, unhandled KeyError, and quadratic nested loop.
"""

def calculate_conversion_rate(signups: int, visitors: int) -> float:
    # BUG 1: Potential ZeroDivisionError when visitors == 0
    return (signups / visitors) * 100.0


def extract_user_tier(payload: dict) -> str:
    # BUG 2: KeyError if 'tier' key is missing in unauthenticated requests
    return payload["subscription"]["tier"].upper()


def find_common_elements(list_a: list, list_b: list) -> list:
    # BUG 3: Inefficient O(N*M) lookups instead of set intersection
    common = []
    for item in list_a:
        if item in list_b and item not in common:
            common.append(item)
    return common
