# src/build.py
import os
import markdown

CONTENT_DIR = "content"
OUTPUT_DIR = "output"

def main():
    print("Starting static site build...")
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

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
        </style>
    </head>
    <body>
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
            
            final_html = html_template.format(title=post_title, content=html_content)
            
            output_filename = filename.replace(".md", ".html")
            output_filepath = os.path.join(OUTPUT_DIR, output_filename)
            
            with open(output_filepath, "w") as f:
                f.write(final_html)
            print(f"-> Built {output_filepath}")

    print("Build finished successfully.")

if __name__ == "__main__":
    main()
