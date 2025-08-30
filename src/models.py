from dataclasses import dataclass
from datetime import date


@dataclass
class Post:
    """Represents a single blog post."""

    title: str
    date: date
    content_html: str
    slug: str
