# src/parsers.py (Final Corrected Version)
import frontmatter
import markdown
import html  # <-- IMPORT THE HTML LIBRARY
from pathlib import Path
from src.models import Post
from datetime import date


def parse_markdown_file(filepath: Path) -> Post:
    post_fm = frontmatter.load(filepath)

    extensions = ["pymdownx.superfences", "codehilite"]

    # This version now uses html.unescape to reverse any unwanted HTML
    # entity conversion performed by the markdown parser on the raw source.
    extension_configs = {
        "pymdownx.superfences": {
            "custom_fences": [
                {
                    "name": "mermaid",
                    "class": "mermaid",
                    "format": lambda source, language, css_class, options, md, **kwargs: f'<pre class="mermaid">{html.unescape(source)}</pre>',
                }
            ]
        }
    }

    html_content = markdown.markdown(
        post_fm.content, extensions=extensions, extension_configs=extension_configs
    )

    metadata = post_fm.metadata

    return Post(
        title=metadata.get("title", "Untitled Post"),
        date=metadata.get("date", date(2025, 1, 1)),
        content_html=html_content,
        content_raw=post_fm.content,
        slug=filepath.stem,
        template=metadata.get("template"),
        type=metadata.get("type", "post"),
        tags=metadata.get("tags", []),
        description=metadata.get("description"),
        keywords=metadata.get("keywords", []),
    )
