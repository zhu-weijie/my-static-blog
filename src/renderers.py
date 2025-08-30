from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from urllib.parse import quote_plus
from src.models import Post, Tag, Category
from src.paginator import Paginator


def safe_urlencode(value):
    """A Jinja2 filter that URL-encodes a string, handling None safely."""
    if value is None:
        return ""
    return quote_plus(str(value))


class Renderer:
    def __init__(self, template_dir: Path):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.filters["urlencode"] = safe_urlencode

    def render_post(self, post: Post, site_url: str, output_dir: Path):
        """Renders a single post to an HTML file inside its own directory."""
        template = self.env.get_template("post.html")
        rendered_html = template.render(post=post, site_url=site_url)

        # Create the post's directory, e.g., output/posts/post-slug/
        post_dir = output_dir / "posts" / post.slug
        post_dir.mkdir(parents=True, exist_ok=True)

        # Write the content to index.html within that directory
        output_file = post_dir / "index.html"
        output_file.write_text(rendered_html)

    def render_paginated_index(self, paginator: Paginator, output_dir: Path):
        """Renders all paginated index pages."""
        template = self.env.get_template("index.html")

        for page_data in paginator:
            page_num = page_data["page_num"]

            # Determine the output path
            if page_num == 1:
                page_dir = output_dir
            else:
                page_dir = output_dir / "page" / str(page_num)

            page_dir.mkdir(parents=True, exist_ok=True)
            output_file = page_dir / "index.html"

            rendered_html = template.render(page=page_data)
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

    def render_sitemap(self, posts: list[Post], site_url: str, output_dir: Path):
        """Renders the sitemap.xml file."""
        template = self.env.get_template("sitemap.xml")
        rendered_xml = template.render(posts=posts, site_url=site_url)

        output_file = output_dir / "sitemap.xml"
        output_file.write_text(rendered_xml)

    def render_rss(
        self,
        posts: list[Post],
        site_title: str,
        site_description: str,
        site_url: str,
        output_dir: Path,
    ):
        """Renders the rss.xml file."""
        template = self.env.get_template("rss.xml")
        rendered_xml = template.render(
            posts=posts,
            site_title=site_title,
            site_description=site_description,
            site_url=site_url,
        )

        output_file = output_dir / "rss.xml"
        output_file.write_text(rendered_xml)

    def render_page(self, page: Post, output_dir: Path):
        """Renders a standalone page (like Contact)."""
        template = self.env.get_template("page.html")
        rendered_html = template.render(page=page)

        # Create the page's directory, e.g., output/contact/
        page_dir = output_dir / page.slug
        page_dir.mkdir(parents=True, exist_ok=True)

        output_file = page_dir / "index.html"
        output_file.write_text(rendered_html)
