from typing import List, Optional
from sqlalchemy.orm import Session

from aurora.database import models


def get_strings(db: Session, offset: int = 0, limit: int = 50) -> List[models.String]:

    """Get strings.

    Returns a list of strings in the database.

    Args:
        db (Session): Database session.
        offset (int): Offset from which the query starts.
        limit (int): Max number of strings returned in a single query.

    Returns:
        List(String) List of string objects.

    """

    strings = db.query(models.String).offset(offset).limit(limit).all()
    return strings


def get_unique_strings(
    db: Session, offset: int = 0, limit: int = 50
) -> List[models.String]:

    """Get unique strings.

    Returns a list of distinct strings in the database.

    Args:
        db (Session): Database session.
        offset (int): Offset from which the query starts.
        limit (int): Max number of strings returned in a single query.

    Returns:
        List(String) List of unique string objects.

    """

    strings = (
        db.query(models.String)
        .distinct(models.String.sha256)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return strings


def get_string_by_sha256(db: Session, sha256: str) -> Optional[models.String]:

    """Get string by SHA256 hash.

    Returns a string with a specified SHA256 hash.

    Args:
        db (Session): Database session.
        sha256 (str): SHA256 hash of the string.

    Returns:
        String String with the specified hash.

    """

    string = db.query(models.String).filter(models.String.sha256 == sha256).first()

    return string


def get_string_by_value(db: Session, value: str) -> Optional[models.String]:

    """Get string by SHA256 hash.

    Returns a string with a specified SHA256 hash.

    Args:
        db (Session): Database session.
        value (str): Value hash of the string.

    Returns:
        String String with the specified hash.

    """

    string = db.query(models.String).filter(models.String.value == value).first()

    return string


def add_string(db: Session, value: str, sha256: str, heuristic: str) -> models.String:

    """Add string.

    Add new string to the database.

    Args:
       db (Session): Database session.
       value (str): Value of the string.
       sha256 (str): SHA256 hash of the string.
       heuristic (str): Heuristic name from which the string was recovered.

    Returns:
        String Newly added string.

    """

    string = models.String(value=value, sha256=sha256, heuristic=heuristic)

    db.add(string)

    return string
