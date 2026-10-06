"""PDF rendering must preserve manuscript and previous successful artifacts."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
from pypdf import PdfReader

SCRIPT = Path(__file__).resolve().parents[1] / "build_paper.py"
SPEC = importlib.util.spec_from_file_location("build_paper", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def test_refuses_to_overwrite_manuscript(tmp_path: Path) -> None:
    manuscript = tmp_path / "paper.md"
    original = "# A paper\n\nSource text.\n"
    manuscript.write_text(original)
    with pytest.raises(ValueError, match="Markdown source"):
        builder.build(manuscript, manuscript)
    assert manuscript.read_text() == original


def test_pdf_contains_title_table_and_list(tmp_path: Path) -> None:
    manuscript = tmp_path / "paper.md"
    manuscript.write_text(
        "# Example title\n\n## Methods\n\nA **clear** method.\n\n"
        "| Result | Value |\n|---|---|\n| Count | 3 |\n\n- First item\n"
    )
    output = tmp_path / "paper.pdf"
    builder.build(manuscript, output)
    text = "\n".join(page.extract_text() for page in PdfReader(output).pages)
    assert "Example title" in text
    assert "Methods" in text
    assert "Count" in text and "First item" in text


def test_failed_render_preserves_previous_pdf(tmp_path: Path) -> None:
    manuscript = tmp_path / "paper.md"
    manuscript.write_text("# First version\n")
    output = tmp_path / "paper.pdf"
    builder.build(manuscript, output)
    previous = output.read_bytes()
    manuscript.write_text("# Broken draft\n\n![Absent](absent.png)\n")
    with pytest.raises(OSError):
        builder.build(manuscript, output)
    assert output.read_bytes() == previous
    assert not list(tmp_path.glob(".working-paper-*.pdf"))
