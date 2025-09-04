import frontmatter
import markdown
from pathlib import Path
from src.models import Post


def parse_markdown_file(filepath: Path) -> Post:
    post_fm = frontmatter.load(filepath)

    extensions = ["pymdownx.superfences", "codehilite"]

    extension_configs = {
        "pymdownx.superfences": {
            "custom_fences": [
                {
                    "name": "mermaid",
                    "class": "mermaid",
                    "format": lambda source, language, css_class, options, md, **kwargs: f'<pre class="mermaid">{source}</pre>',
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
