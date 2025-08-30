from pathlib import Path
from collections import defaultdict
from src.parsers import parse_markdown_file
from src.renderers import Renderer
from src.models import Post, Tag, Category  # Import new models


class SiteBuilder:
    def __init__(self):
        self.content_dir = Path("content")
        self.output_dir = Path("output")
        self.renderer = Renderer(Path("templates"))
        self.site_url = "http://localhost:8080"

    def build(self):
        print("Starting site build...")
        self.output_dir.mkdir(exist_ok=True)

        # 1. Parse all content
        posts = [parse_markdown_file(fp) for fp in self.content_dir.glob("*.md")]
        posts.sort(key=lambda p: p.date, reverse=True)  # Sort posts once
        print(f"Found and parsed {len(posts)} posts.")

        # 2. Group posts by tags and categories
        tags = self._collect_tags(posts)
        categories = self._collect_categories(posts)

        # 3. Render everything
        for post in posts:
            self.renderer.render_post(post, self.output_dir)
        print("Rendered individual posts.")

        self.renderer.render_index(posts, self.output_dir)
        print("Rendered index page.")

        for tag in tags.values():
            self.renderer.render_tag(tag, self.output_dir)
        print(f"Rendered {len(tags)} tag pages.")

        for category in categories.values():
            self.renderer.render_category(category, self.output_dir)
        print(f"Rendered {len(categories)} category pages.")

        self.renderer.render_sitemap(posts, self.site_url, self.output_dir)
        print("Rendered sitemap.xml.")

        print("Site build finished successfully.")

    def _collect_tags(self, posts: list[Post]) -> dict[str, Tag]:
        tags = defaultdict(lambda: Tag(name=""))
        for post in posts:
            for tag_name in post.tags:
                if not tags[tag_name].name:
                    tags[tag_name].name = tag_name
                tags[tag_name].posts.append(post)
        return tags

    def _collect_categories(self, posts: list[Post]) -> dict[str, Category]:
        categories = defaultdict(lambda: Category(name=""))
        for post in posts:
            if post.category:
                cat_name = post.category
                if not categories[cat_name].name:
                    categories[cat_name].name = cat_name
                categories[cat_name].posts.append(post)
        return categories
