import os


def is_windows():
    """Detects whether the operating system is windows.

    Returns:
        windows detected
    """
    return os.name == "nt"


def fix_lims_path(path):
    """Fixes a lims filepath on the network to work on windows.

    Returns:
        fixed path
    """
    if path.startswith("/allen"):
        return "/" + path

    return path


def is_valid_exp_id(value: str) -> bool:
    """Checks whether or not an experiment id is valid.

    Returns:
        is a valid experiment id
    """
    return value.isdigit()
