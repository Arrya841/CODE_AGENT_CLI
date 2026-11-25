from http.client import FORBIDDEN
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN_NAMES = {".venv", ".git", ".env"}

def validate_path(directory="."):
    requested_path = (PROJECT_ROOT / directory).resolve()
    if not requested_path.is_relative_to(PROJECT_ROOT):
        raise PermissionError(
            "Access denied: Path is outside the project workspace."
        )
    relative_path = requested_path.relative_to(PROJECT_ROOT)
    if any(
        part.lower() in FORBIDDEN_NAMES
        for part in relative_path.parts
    ):
        raise PermissionError(
            "Access denied: Forbidden Files or Directories"
        )
    
    return requested_path