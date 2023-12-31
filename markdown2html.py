import sys
import os
import markdown
import re
import hashlib

def convert_markdown_to_html(markdown_file, output_file):
    try:
        with open(markdown_file, 'r') as md_file:
            md_content = md_file.read()
            html_content = markdown.markdown(md_content, extensions=['markdown.extensions.extra'])

            # Parse custom syntax [[MD5]]
            html_content = re.sub(r'\[\[(.*?)\]\]', lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), html_content)

            # Parse custom syntax ((remove))
            html_content = re.sub(r'\(\((.*?)\)\)', lambda x: x.group(1).replace('c', '').replace('C', ''), html_content, flags=re.IGNORECASE)

        with open(output_file, 'w') as html_file:
            html_file.write(html_content)
    except FileNotFoundError:
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(markdown_file, output_file)
    sys.exit(0)
