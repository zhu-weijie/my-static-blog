from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from src.models import Post, Tag, Category


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

    def render_tag(self, tag: Tag, output_dir: Path):
        output_dir_tag = output_dir / "tags"
        output_dir_tag.mkdir(exist_ok=True)
        template = self.env.get_template("tag.html")
        title = f"Posts tagged: {tag.name}"
        rendered_html = template.render(posts=tag.posts, title=title)
        output_file = output_dir_tag / f"{tag.slug}.html"
        output_file.write_text(rendered_html)

    def render_category(self, category: Category, output_dir: Path):
        output_dir_cat = output_dir / "categories"
        output_dir_cat.mkdir(exist_ok=True)
        template = self.env.get_template("category.html")
        title = f"Posts in category: {category.name}"
        rendered_html = template.render(posts=category.posts, title=title)
        output_file = output_dir_cat / f"{category.slug}.html"
        output_file.write_text(rendered_html)
