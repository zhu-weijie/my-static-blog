from pathlib import Path
from src.parsers import parse_markdown_file


def run():
    print("Build process initiated...")

    content_dir = Path("content")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # 1. Discover and parse all content
    posts = []
    for filepath in content_dir.glob("*.md"):
        print(f"Parsing {filepath.name}...")
        post = parse_markdown_file(filepath)
        posts.append(post)

    # 2. Verify by printing titles to the console
    print("\nSuccessfully parsed posts:")
    for post in posts:
        print(f"- {post.title} (Date: {post.date})")

    # 3. Write a temporary file to verify the Caddy server is working
    with open(output_dir / "index.html", "w") as f:
        f.write("<h1>Parsing successful! Check your docker logs.</h1>")

    print("\nBuild process finished.")
