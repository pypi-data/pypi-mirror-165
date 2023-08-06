from typing import Dict, List, Optional, Tuple

import logging

from psycopg2 import connect, extensions, extras

from .config import allen_config_auto_discovery
from .dataclasses import Query
from .exceptions import LimsError
from .local_paths import get_suffixes, local_path_to_Query
from .utils import fix_lims_path, is_valid_exp_id, is_windows
from .wkft import get_wkft_names, wkft_to_Query

logger = logging.getLogger(__name__)


def run_query(cursor: extensions.cursor, query: Query) -> list[str]:
    """Runs a lims query.

    Args:
        cursor: lims postgresql cursor instance
        query: Query instance to run

    Returns:
        List of filepaths to assets on lims.
    """
    cursor.execute(query.query_str)
    filtered = []
    for row in cursor.fetchall():
        for (key, value) in query.filters:
            if row[key] != value:
                break
        else:
            filtered.append(row[query.return_name])
    return filtered


def _init_cursor(db_uri: str) -> extensions.cursor:
    """Initializes a connection to the lims database."""
    logger.info("Connecting to database uri: %s..." % db_uri)
    con = connect(db_uri)
    con.set_session(readonly=True, autocommit=True)
    return con.cursor(
        cursor_factory=extras.RealDictCursor,
    )


def _resolve_query(
    exp_id: Optional[str] = None,
    wkft: Optional[str] = None,
    local_path: Optional[str] = None,
) -> Query:
    """Resolves a combination of experiment meta info to a query to be executed on lims."""
    if wkft and exp_id:
        if not is_valid_exp_id(exp_id):
            raise LimsError("Invalid experiment id: %s" % exp_id)
        query = wkft_to_Query(wkft, exp_id)
    elif local_path:
        query = local_path_to_Query(local_path, exp_id)
    else:
        raise LimsError("Invalid number of arguments supplied.")

    return query


def find_files(
    db_uri: Optional[str] = None,
    exp_id: Optional[str] = None,
    wkft: Optional[str] = None,
    local_path: Optional[str] = None,
) -> list[str]:
    """Finds all files associated with a combination of experiment meta info.

    Args:
        db_uri: lims database uri
        exp_id: lims experiment id associated with the files
        wkft: well known file type name associated with the files you want to find
        local_path: local filepath of a file you want to find on lims

    Returns:
        A list of filepaths

    Note:
        - The following combinations of meta info are supported
            - ``exp_id`` and ``wkft``
            - ``local_path``
        - A ``local_path`` can be prefixed with * but an experiment id will need to be supplied
        - If no ``db_uri`` is supplied, will attempt ``allen_config_auto_discovery``
    """
    if db_uri is None:
        logger.info("No db_uri supplied, using allen config auto discovery...")
        db_uri = allen_config_auto_discovery("lims_db_uri")
        logger.info("Resolved db_uri: %s" % db_uri)

    query = _resolve_query(exp_id=exp_id, wkft=wkft, local_path=local_path)
    logger.info("Resolved query: %s" % query)

    with _init_cursor(db_uri) as cursor:
        results = run_query(cursor, query)

    if is_windows():
        logger.info(
            "Windows detected. Fixing paths for windows. Paths before: %s" % results
        )
        fixed = [fix_lims_path(result) for result in results]
        logger.info("Paths after: %s" % fixed)
        return fixed

    return results
