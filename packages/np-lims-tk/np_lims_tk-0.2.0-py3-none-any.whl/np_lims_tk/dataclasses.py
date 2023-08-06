from typing import Any, List, Tuple

from dataclasses import dataclass


@dataclass
class Query:

    """Abstraction of query to be executed on lims database."""

    query_str: str
    filters: list[tuple[str, Any]]
    return_name: str
