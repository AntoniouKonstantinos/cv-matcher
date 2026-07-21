import os
import pytest
from app.extraction import allowed_file, extract_text


def test_allowed_file_accepts_valid_extensions():
    assert allowed_file('resume.pdf') is True
    assert allowed_file('resume.docx') is True
    assert allowed_file('resume.txt') is True


def test_allowed_file_is_case_insensitive():
    assert allowed_file('resume.PDF') is True
    assert allowed_file('resume.DocX') is True


def test_allowed_file_rejects_invalid_extensions():
    assert allowed_file('resume.exe') is False
    assert allowed_file('resume.jpg') is False


def test_allowed_file_rejects_no_extension():
    assert allowed_file('resume') is False


def test_allowed_file_handles_multiple_dots():
    assert allowed_file('my.resume.final.pdf') is True


def test_extract_text_from_txt(tmp_path):
    filepath = tmp_path / "sample.txt"
    filepath.write_text("Python developer with Flask experience.")

    result = extract_text(str(filepath))

    assert result == "Python developer with Flask experience."


def test_extract_text_unsupported_extension(tmp_path):
    filepath = tmp_path / "sample.xyz"
    filepath.write_text("some content")

    with pytest.raises(ValueError):
        extract_text(str(filepath))