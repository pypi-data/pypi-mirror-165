from pathlib import Path
import pytest

from event_data_logging.file_handling import validate_filename


def test_validate_filename():
    """Test if filename is correctly incremented if file exists"""

    input_filename = "data/non_existing_file.json"

    assert Path(input_filename).absolute() == validate_filename(input_filename)

    input_filename = "test_data/existing_file.json"
    goal_filename = Path("test_data/existing_file_2.json").absolute()
    assert goal_filename == validate_filename(input_filename)


def test_validate_filename_folders():
    """test if new folder is created. Folder is removed afterwards"""

    filename = "a/testfile"
    try:
        output_filename = validate_filename(filename)

    finally:
        Path.rmdir(Path(filename).parent)


def test_validate_filename_permission_error():
    """Test that exception is raised of no permission to create parent directory"""

    filename = "/temp1/testfile"

    with pytest.raises(Exception) as e_info:
        output_filename = validate_filename(filename)
    assert str(e_info.value) == f"failed to make {Path(filename).parent}"
