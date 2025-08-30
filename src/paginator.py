from typing import List
from src.models import Post


class Paginator:
    def __init__(self, posts: List[Post], per_page: int):
        self.posts = posts
        self.per_page = per_page
        self.total_posts = len(posts)
        self.total_pages = (self.total_posts + self.per_page - 1) // self.per_page

    def get_page(self, page_num: int):
        """Returns the posts for a given page number."""
        start_index = (page_num - 1) * self.per_page
        end_index = start_index + self.per_page
        return self.posts[start_index:end_index]

    def __iter__(self):
        """Allows iterating through the pages."""
        for page_num in range(1, self.total_pages + 1):
            yield {
                "posts": self.get_page(page_num),
                "page_num": page_num,
                "total_pages": self.total_pages,
                "has_next": page_num < self.total_pages,
                "has_prev": page_num > 1,
                "next_page_num": page_num + 1,
                "prev_page_num": page_num - 1,
            }
