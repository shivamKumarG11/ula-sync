import uuid
from datetime import date


def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def validate_date_range(start: date, end: date, label: str = "date range") -> None:
    from app.utils.errors import AppError

    if end < start:
        raise AppError(f"End date must be >= start date for {label}", 400)


def validate_date_within_range(
    check_date: date, range_start: date, range_end: date, label: str = "date"
) -> None:
    from app.utils.errors import AppError

    if not (range_start <= check_date <= range_end):
        raise AppError(f"{label} must be between {range_start} and {range_end}", 400)
