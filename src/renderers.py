from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from src.models import Post


class Renderer:
    def __init__(self, template_dir: Path):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render_post(self, post: Post, output_dir: Path):
        """Renders a single post to an HTML file."""
        template = self.env.get_template("post.html")
        rendered_html = template.render(post=post)

        output_file = output_dir / f"{post.slug}.html"
        output_file.write_text(rendered_html)

    def render_index(self, posts: list[Post], output_dir: Path):
        """Renders the index page."""
        template = self.env.get_template("index.html")

        # Sort posts by date, newest first
        sorted_posts = sorted(posts, key=lambda p: p.date, reverse=True)

        rendered_html = template.render(posts=sorted_posts)

        output_file = output_dir / "index.html"
        output_file.write_text(rendered_html)
