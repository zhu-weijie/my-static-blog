import os
import markdown

CONTENT_DIR = "content"
OUTPUT_DIR = "output"

def main():
    print("Starting static site build...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # A list to store info about each post
    all_posts = []

    # Basic HTML template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
            .post-link {{ font-size: 1.2rem; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {content}
    </body>
    </html>
    """

    # Process each markdown file
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(CONTENT_DIR, filename)
            with open(filepath, "r") as f:
                md_content = f.read()
            
            html_content = markdown.markdown(md_content)
            post_title = filename.replace(".md", "").replace("-", " ").title()
            
            # Use the post's own title for the page title
            final_html = html_template.format(title=post_title, content=html_content)
            
            output_filename = filename.replace(".md", ".html")
            output_filepath = os.path.join(OUTPUT_DIR, output_filename)
            
            with open(output_filepath, "w") as f:
                f.write(final_html)
            print(f"-> Built {output_filepath}")

            # Add post info to our list for the index page
            all_posts.append({
                "title": post_title,
                "link": output_filename
            })

    # --- NEW: Build the index.html page ---
    print("Building index page...")
    index_links_html = "<ul>"
    for post in sorted(all_posts, key=lambda p: p['title']): # Sort posts alphabetically
        index_links_html += f'<li><a href="{post["link"]}" class="post-link">{post["title"]}</a></li>'
    index_links_html += "</ul>"
    
    index_final_html = html_template.format(title="My Awesome Blog", content=index_links_html)
    
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w") as f:
        f.write(index_final_html)
    print("-> Built index.html")

    print("Build finished successfully.")

if __name__ == "__main__":
    main()
