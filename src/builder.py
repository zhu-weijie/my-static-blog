from pathlib import Path
from src.parsers import parse_markdown_file
from src.renderers import Renderer


class SiteBuilder:
    def __init__(self):
        self.content_dir = Path("content")
        self.output_dir = Path("output")
        self.template_dir = Path("templates")
        self.renderer = Renderer(self.template_dir)

    def build(self):
        print("Starting site build...")
        self.output_dir.mkdir(exist_ok=True)

        posts = [parse_markdown_file(fp) for fp in self.content_dir.glob("*.md")]
        print(f"Found and parsed {len(posts)} posts.")

        for post in posts:
            self.renderer.render_post(post, self.output_dir)
        print("Rendered individual posts.")

        self.renderer.render_index(posts, self.output_dir)
        print("Rendered index page.")

        print("Site build finished successfully.")
