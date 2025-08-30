from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List


@dataclass
class Post:
    """Represents a single blog post."""

    title: str
    date: date
    content_html: str
    slug: str
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
