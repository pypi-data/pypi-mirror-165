from typing import Dict, List, Optional, Tuple

import logging
import os

from .dataclasses import Query
from .exceptions import LimsError
from .wkft import wkft_to_Query

logger = logging.getLogger(__name__)

WILD_CARD = "*"

SUFFIX_TO_WKFT_MAP = {
    "_platformD1.json": "EcephysPlatformFile",
    ".sync": "EcephysRigSync",
    "_surface-image6-right.png": "EcephysPreInsertionRight",
    "_surface-image6-left.png": "EcephysPreInsertionLeft",
    "_surface-image5-left.png": "EcephysPreExperimentLeft",
    "_surface-image5-right.png": "EcephysPreExperimentRight",
    "_surface-image4-left.png": "EcephysPostStimulusLeft",
    "_surface-image4-right.png": "EcephysPostStimulusRight",
    "_surface-image3-right.png": "EcephysPostInsertionRight",
    "_surface-image3-left.png": "EcephysPostInsertionLeft",
    "_surface-image2-right.png": "EcephysPostExperimentRight",
    "_surface-image2-left.png": "EcephysPostExperimentLeft",
    ".overlay.png": "EcephysOverlayImage",
    ".insertionLocation.png": "EcephysInsertionLocationImage",
    ".fiducial.png": "EcephysFiducialImage",
    "_surface-image1-right.png": "EcephysBrainSurfaceRight",
    "_surface-image1-left.png": "EcephysBrainSurfaceLeft",
    ".behavior.pkl": "StimulusPickle",
    ".mapping.pkl": "MappingPickle",
    ".areaClassifications.csv": "EcephysAreaClassifications",
    ".behavior.json": "RawBehaviorTrackingVideoMetadata",
    ".behavior.mp4": "RawBehaviorTrackingVideo",
    ".eye.json": "RawEyeTrackingVideoMetadata",
    ".eye.mp4": "RawEyeTrackingVideo",
    ".face.json": "RawFaceTrackingVideoMetadata",
    ".face.mp4": "RawFaceTrackingVideo",
    ".motor-locs.csv": "NewstepConfiguration",
    ".replay.pkl": "EcephysReplayStimulus",
    ".opto.pkl": "OptoPickle",
    "_surgeryNotes.json": "EcephysSurgeryNotes",
}

SUFFIXES = list(SUFFIX_TO_WKFT_MAP.keys())
"""Names of supported suffixes for local_paths.
"""


def dir_to_experiment_id(path: str, suffix: str) -> str:
    """Currently unsupported"""
    raise LimsError("Directories not supported yet :0...")


def path_to_experiment_id(path: str, suffix: str) -> str:
    """Extracts an experiment id from a structured filepath.

    :param path: structured filepath
    :param suffix: suffix of the filepath
    :returns: extracted experiment id
    """
    if os.path.isdir(path):
        logger.info("Directory detected, using dir_to_meta.")
        return dir_to_meta(path, suffix)

    filename = os.path.basename(path)
    meta_str = filename.removesuffix(suffix)

    if meta_str == WILD_CARD:
        logger.info("Wild card detected Not inferring exp id. path: %s" % path)
        return

    values = meta_str.split("_")

    if len(values) != 3:  # assume valid meta_strs will be 3 items
        logger.info("Meta could not be parsed for: %s" % path)
        return

    return values[0]


def deserialize_path(path: str) -> tuple[Optional[str], str]:
    """Deserializes a structured filepath into an experiment id and
    wkft

    :param path: structured filepath
    :returns: experiment id if it could be extracted and wkft

    note:: wkft will be one of the well known file types supported by lims
    """
    for (
        suffix,
        wkft,
    ) in SUFFIX_TO_WKFT_MAP.items():
        if path.endswith(suffix):
            return (
                path_to_experiment_id(path, suffix),
                wkft,
            )
    else:
        raise LimsError("Unsupported path: %s" % path)


def local_path_to_Query(path: str, experiment_id: Optional[str] = None) -> Query:
    """Transforms a local filepath into a :class:`Query`.

    :param path: path to the file
    :param experiment_id: lims experiment id

    :returns: resolved query
    """
    inferred_experiment_id, wkft = deserialize_path(
        normalize_path(path),
    )

    if not experiment_id and not inferred_experiment_id:
        raise LimsError(
            "No experiment id supplied and no experiment id could be inferred. path: %s"
            % path
        )

    return wkft_to_Query(
        wkft, experiment_id or inferred_experiment_id
    )  # choose explicit experiment id first


def normalize_path(path: str) -> str:
    """Transform a local path into parent_dir and filename."""
    if path.startswith(WILD_CARD):
        logger.info("Wild card detected, not normalizing. path: %s" % path)
        return path
    logger.info("Normalizing path: %s" % path)
    dirname, filename = path.split("\\")[-2:]
    normalized = os.path.join(dirname, filename)
    logger.info("Normalized path: %s" % normalized)
    return normalized


def get_suffixes() -> list[str]:
    """Gets a list of supported filename suffixes.

    Returns:
        list of filename suffixes
    """
    return list(SUFFIX_TO_WKFT_MAP.keys())
