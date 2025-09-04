import shutil
import json
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict
from src.parsers import parse_markdown_file
from src.renderers import Renderer
from src.models import Post, Tag, Category
from src.paginator import Paginator


class SiteBuilder:
    def __init__(self):
        self.content_dir = Path("content")
        self.output_dir = Path("output")
        self.renderer = Renderer(Path("templates"))
        self.site_title = "Zhu Weijie's Weblog"
        self.site_description = "A blog about technology and web development."
        self.pages_dir = Path("pages")
        self.site_url = "https://zhu-weijie.github.io"
        self.static_dir = Path("static")
        self.posts_per_page = 20

    def build(self):
        print("Starting site build...")

        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(exist_ok=True)

        if self.static_dir.exists():
            shutil.copytree(self.static_dir, self.output_dir / "static")
            print("Copied static files.")

        # 1. First, parse ALL markdown content from all source directories
        all_content = [parse_markdown_file(fp) for fp in self.content_dir.glob("*.md")]
        pages = [parse_markdown_file(fp) for fp in self.pages_dir.glob("*.md")]

        # 2. Next, filter the content into different types
        posts = sorted(
            [p for p in all_content if p.type == "post"],
            key=lambda p: p.date,
            reverse=True,
        )
        diagrams = sorted(
            [p for p in all_content if p.type == "diagram"],
            key=lambda p: p.date,
            reverse=True,
        )

        print(f"Found and parsed {len(posts)} posts.")
        print(f"Found and parsed {len(diagrams)} diagrams.")
        print(f"Found and parsed {len(pages)} standalone pages.")

        # 3. Now, use the 'posts' list for all the original build steps
        self._calculate_related_posts(posts)
        tags = self._collect_tags(posts)
        categories = self._collect_categories(posts)

        # Render pages and posts (now includes diagrams as they are also 'Post' objects)
        for page in pages:
            self.renderer.render_page(page, self.output_dir)
        for item in all_content:
            self.renderer.render_post(item, self.site_url, self.output_dir)
        print("Rendered individual content pages.")

        # Tag and Category pages are still based on 'posts'
        for tag in tags.values():
            self.renderer.render_tag(tag, self.output_dir)
        for category in categories.values():
            self.renderer.render_category(category, self.output_dir)
        print(f"Rendered {len(tags)} tag and {len(categories)} category pages.")

        self.renderer.render_diagrams_index(diagrams, self.output_dir)
        print("Rendered diagrams index page.")

        # The main index and feeds are still based on 'posts'
        paginator = Paginator(posts, self.posts_per_page)
        self.renderer.render_paginated_index(paginator, self.output_dir)
        print(f"Rendered {paginator.total_pages} main index pages.")

        self.renderer.render_sitemap(posts, self.site_url, self.output_dir)
        self.renderer.render_rss(
            posts=posts,
            site_title=self.site_title,
            site_description=self.site_description,
            site_url=self.site_url,
            output_dir=self.output_dir,
        )
        print("Rendered sitemap and RSS feed for posts.")

        # The search index should include EVERYTHING
        self._generate_search_index(all_content)
        print("Generated global search index.")

        print("Site build finished successfully.")

    def _generate_search_index(self, posts: list[Post]):
        """Generates a JSON search index from all posts."""
        search_data = []
        for post in posts:
            # Combine title, tags, category, and content into one string
            tags_text = " ".join(post.tags)
            category_text = post.category or ""

            soup = BeautifulSoup(post.content_html, "html.parser")
            plain_text_content = soup.get_text()

            # The final searchable content
            searchable_content = (
                f"{post.title} {tags_text} {category_text} {plain_text_content}"
            )

            search_data.append(
                {
                    "title": post.title,
                    "url": post.permalink,
                    "content": searchable_content,
                }
            )

        output_file = self.output_dir / "search-index.json"
        output_file.write_text(json.dumps(search_data, indent=2))

    def _calculate_related_posts(self, all_posts: list[Post], max_related: int = 3):
        """Calculates related posts based on shared tags."""

        # Create a lookup map from slug to Post object for easy access later
        post_map = {p.slug: p for p in all_posts}

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
                    # Use the slug (a string) as the key, which is hashable
                    if related_post.slug != post.slug:
                        scores[related_post.slug] += 1

            # Sort the slugs by score in descending order
            sorted_related_slugs = sorted(scores, key=scores.get, reverse=True)

            # Assign the top N posts to the related_posts field by looking them up in our map
            post.related_posts = [
                post_map[slug] for slug in sorted_related_slugs[:max_related]
            ]

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
