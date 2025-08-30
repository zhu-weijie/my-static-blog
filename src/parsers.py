import frontmatter
import markdown
from pathlib import Path
from src.models import Post


def parse_markdown_file(filepath: Path) -> Post:
    """Parses a markdown file with frontmatter and returns a Post object."""
    post_fm = frontmatter.load(filepath)

    # Convert markdown content to HTML
    html_content = markdown.markdown(post_fm.content)

    # Extract metadata, ensuring a default for any missing keys if needed
    metadata = post_fm.metadata

    # Create the Post object
    return Post(
        title=metadata.get("title", "Untitled Post"),
        date=metadata.get("date"),
        content_html=html_content,
        slug=filepath.stem,  # e.g., "2025-08-28-my-first-post"
    )
