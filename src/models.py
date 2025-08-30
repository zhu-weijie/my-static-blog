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

    @property
    def permalink(self) -> str:
        """Generates the permanent link for the post."""
        return f"/posts/{self.slug}/"


@dataclass
class Tag:
    """Represents a single tag and all its posts."""

    name: str
    posts: List[Post] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "-")


@dataclass
class Category:
    """Represents a single category and all its posts."""

    name: str
    posts: List[Post] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "-")
