import pytest

from app.ingestion.validator import DocumentValidationError, validate_pdf


def test_validate_pdf_accepts_valid_pdf_signature() -> None:
    content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    validate_pdf(content, filename="sample.pdf", max_size_bytes=1024)


def test_validate_pdf_rejects_non_pdf_content() -> None:
    with pytest.raises(DocumentValidationError) as exc:
        validate_pdf(b"not-a-pdf", filename="bad.txt", max_size_bytes=1024)
    assert exc.value.error_code == "INVALID_FORMAT"


def test_validate_pdf_rejects_oversized_file() -> None:
    content = b"%PDF-" + b"x" * 32
    with pytest.raises(DocumentValidationError) as exc:
        validate_pdf(content, filename="big.pdf", max_size_bytes=10)
    assert exc.value.error_code == "FILE_TOO_LARGE"


def test_validate_pdf_rejects_empty_file() -> None:
    with pytest.raises(DocumentValidationError) as exc:
        validate_pdf(b"", filename="empty.pdf", max_size_bytes=1024)
    assert exc.value.error_code == "EMPTY_FILE"
