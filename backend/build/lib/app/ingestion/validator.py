from dataclasses import dataclass

PDF_MAGIC_BYTES = b"%PDF-"


@dataclass(frozen=True)
class DocumentValidationError(Exception):
    message: str
    error_code: str

    def __str__(self) -> str:
        return self.message


def validate_pdf(content: bytes, filename: str, max_size_bytes: int) -> None:
    if not content:
        raise DocumentValidationError("Uploaded file is empty", "EMPTY_FILE")

    if not content.startswith(PDF_MAGIC_BYTES):
        raise DocumentValidationError(
            f"File '{filename}' is not a valid PDF",
            "INVALID_FORMAT",
        )

    if len(content) > max_size_bytes:
        raise DocumentValidationError(
            f"File '{filename}' exceeds the maximum allowed size",
            "FILE_TOO_LARGE",
        )
