"""file_handling.py

Contains: 
    - validate_filename: performs checks to see if file and parent directory 
        already exist
"""

from pathlib import Path
from typing import Union


def validate_filename(goal_filename: Union[str, Path]) -> Path:
    """Performs several checks on goal_filename:
        - attempts to create parent folder recursively if it  does not exist
        - if file exists, increments a suffix counter until the name is free and
            returns file_path with incremented index.

    Args:
        goal_filename (Union[str, Path])

    Raises:
        PermissionError: Cannot create desired directory

    Returns:
        Path: actual file path to which can be written
    """
    # File shouldn't exist, but if it does, add a number to the
    # end until the name is free.
    file_nth: int = 2
    file_path: Path = Path(goal_filename).resolve()

    file_stem = file_path.stem

    directory: Path = file_path.parent
    # path does not exist, try to make
    if not directory.exists():
        try:
            Path.mkdir(directory, parents=True)
        except:
            raise PermissionError(f"failed to make {directory}")

    while file_path.exists():
        file_path = file_path.with_name(f"{file_stem}_{file_nth}").with_suffix(
            file_path.suffix
        )
        file_nth += 1

    return file_path
