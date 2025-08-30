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
        content_raw=post_fm.content,
        slug=filepath.stem,
        template=metadata.get("template"),
        category=metadata.get("category"),
        tags=metadata.get("tags", []),
        description=metadata.get("description"),
        keywords=metadata.get("keywords", []),
    )
