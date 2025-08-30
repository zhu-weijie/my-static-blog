import frontmatter
import markdown
from pathlib import Path
from src.models import Post


def parse_markdown_file(filepath: Path) -> Post:
    """Parses a markdown file with frontmatter and returns a Post object."""
    post_fm = frontmatter.load(filepath)
    html_content = markdown.markdown(post_fm.content)
    metadata = post_fm.metadata

    return Post(
        title=metadata.get("title", "Untitled Post"),
        date=metadata.get("date"),
        content_html=html_content,
        slug=filepath.stem,
        # Extract the new metadata, providing safe defaults
        category=metadata.get("category"),
        tags=metadata.get("tags", []),
    )
