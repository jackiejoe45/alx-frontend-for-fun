#!/usr/bin/python3
"""
A script to convert Markdown to HTML.
"""

import sys
import os
import re
import hashlib

def markdown_to_html(input_file, output_file):
    """
    Convert Markdown file to HTML file.
    """
    with open(input_file, 'r') as f:
        content = f.read()

    # Convert headings
    for i in range(6, 0, -1):
        pattern = r'^{} (.+)$'.format('#' * i)
        content = re.sub(pattern, r'<h{0}>\1</h{0}>'.format(i), content, flags=re.MULTILINE)

    # Convert unordered lists
    content = re.sub(r'(?<=\n)- (.+)(?=\n)', r'<li>\1</li>', content)
    content = re.sub(r'(<li>.*</li>\n)+', r'<ul>\n\g<0></ul>\n', content)

    # Convert ordered lists
    content = re.sub(r'(?<=\n)\* (.+)(?=\n)', r'<li>\1</li>', content)
    content = re.sub(r'(<li>.*</li>\n)+', r'<ol>\n\g<0></ol>\n', content)

    # Convert paragraphs
    content = re.sub(r'(?<=\n\n)(.+?)(?=\n\n)', r'<p>\n\1\n</p>', content)
    content = re.sub(r'\n(?!<)', r'<br/>\n', content)

    # Convert bold and italic
    content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
    content = re.sub(r'__(.+?)__', r'<em>\1</em>', content)

    # Convert MD5
    def md5_replace(match):
        return hashlib.md5(match.group(1).encode()).hexdigest()
    content = re.sub(r'\[\[(.+?)\]\]', md5_replace, content)

    # Remove 'c' from content
    def remove_c(match):
        return re.sub(r'[cC]', '', match.group(1))
    content = re.sub(r'\(\((.+?)\)\)', remove_c, content)

    with open(output_file, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(input_file, output_file)
    sys.exit(0)
