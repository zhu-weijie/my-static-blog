from pathlib import Path
from collections import defaultdict
from src.parsers import parse_markdown_file
from src.renderers import Renderer
from src.models import Post, Tag, Category  # Import new models
from src.paginator import Paginator


class SiteBuilder:
    def __init__(self):
        self.content_dir = Path("content")
        self.output_dir = Path("output")
        self.renderer = Renderer(Path("templates"))
        self.site_title = "Zhu Weijie's Weblog"
        self.site_description = "A blog about technology and web development."
        self.site_url = "http://localhost:8080"  # Change this for production
        self.posts_per_page = 1

    def build(self):
        print("Starting site build...")
        self.output_dir.mkdir(exist_ok=True)

        # 1. Parse all content
        posts = [parse_markdown_file(fp) for fp in self.content_dir.glob("*.md")]
        posts.sort(key=lambda p: p.date, reverse=True)  # Sort posts once
        print(f"Found and parsed {len(posts)} posts.")

        self._calculate_related_posts(posts)
        print("Calculated related posts.")

        # 2. Group posts by tags and categories
        tags = self._collect_tags(posts)
        categories = self._collect_categories(posts)

        # 3. Render everything
        for post in posts:
            self.renderer.render_post(post, self.output_dir)
        print("Rendered individual posts.")

        paginator = Paginator(posts, self.posts_per_page)
        self.renderer.render_paginated_index(paginator, self.output_dir)
        print(f"Rendered {paginator.total_pages} index pages.")

        for tag in tags.values():
            self.renderer.render_tag(tag, self.output_dir)
        print(f"Rendered {len(tags)} tag pages.")

        for category in categories.values():
            self.renderer.render_category(category, self.output_dir)
        print(f"Rendered {len(categories)} category pages.")

        self.renderer.render_sitemap(posts, self.site_url, self.output_dir)
        print("Rendered sitemap.xml.")

        self.renderer.render_rss(
            posts=posts,
            site_title=self.site_title,
            site_description=self.site_description,
            site_url=self.site_url,
            output_dir=self.output_dir,
        )
        print("Rendered rss.xml.")

        print("Site build finished successfully.")

    def _calculate_related_posts(self, all_posts: list[Post], max_related: int = 3):
        """Calculates related posts based on shared tags."""
        # Create a dictionary mapping tags to the posts that have them
        tag_map = defaultdict(list)
        for post in all_posts:
            for tag in post.tags:
                tag_map[tag].append(post)

        # Calculate scores for each post
        for post in all_posts:
            scores = defaultdict(int)
            # Find other posts that share tags
            for tag in post.tags:
                for related_post in tag_map[tag]:
                    if related_post is not post:
                        scores[related_post] += 1

            # Sort the posts by score in descending order
            sorted_related = sorted(
                scores.items(), key=lambda item: item[1], reverse=True
            )

            # Assign the top N posts to the related_posts field
            post.related_posts = [p for p, score in sorted_related[:max_related]]

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
