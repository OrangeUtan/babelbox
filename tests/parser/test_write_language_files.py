from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import babelbox


def test():
    languages = {"en_us": {"x": "1", "y": "2"}}
    dest_dir = Path("tests/cli/res")

    expected_langfile_path = Path("tests/cli/res/en_us.json")
    expected_json = {"x": "1", "y": "2"}

    with patch("builtins.open", new=MagicMock()) as mock_open:
        with patch("json.dump", new=MagicMock()) as mock_dump:
            babelbox.write_language_files(dest_dir, languages)

            mock_open.assert_called_once()
            assert mock_open.call_args[0][0] == expected_langfile_path

            mock_dump.assert_called_once()
            assert mock_dump.call_args[0][0] == expected_json
