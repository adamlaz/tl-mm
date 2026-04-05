from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class PersonRecord:
    """Normalized person record from any collector."""
    source: str
    canonical_name: str
    email: Optional[str] = None
    account_id: Optional[str] = None
    title: Optional[str] = None
    team: Optional[str] = None
    manager: Optional[str] = None
    division: Optional[str] = None
    executive: Optional[str] = None
    geography: Optional[str] = None
    status: Optional[str] = None
    aliases: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


KNOWN_BOTS = {
    "AIR",
    "Jenkins",
    "weblate",
    "Bamboobuild",
    "ops",
    "Core Services BA",
    "Cake Cloud Admin",
    "Admin Build",
    "shailabmm",
}
