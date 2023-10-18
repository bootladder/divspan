#!/usr/bin/python
import re
import sys
from html import unescape
from html.parser import HTMLParser
filepath = sys.argv[1]

class Parser:
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.counter = 0

    def get_class_name(self):
        self.counter += 1
        return f"{self.prefix}{self.counter}"
    def parse_content(self, content, prefix="prefix"):
        lines = content.strip().split("\n\n")  # Divided by double newlines
        html_output = []
        div_count = 0
        span_count = 0

        for line in lines:
            div_count += 1
            div_class = f"{prefix}_{div_count}"
            spans = line.split("  ")  # Spans are divided by double spaces
            div_content = []

            for span_text in spans:
                if len(span_text.split()) > 1:  # only wrap in span if more than 1 word
                    span_count += 1
                    span_class = f"{prefix}_{span_count}"
                    div_content.append(f'<span class="{span_class}">{span_text.strip()}</span>')
                else:
                    div_content.append(span_text)

            html_output.append(f'<div class="{div_class}">{"".join(div_content)}</div>')

        return '\n'.join(html_output)




class HTMLFormatter(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indent_level = 0
        self.html = []

    def handle_starttag(self, tag, attrs):
        attributes = ''
        for attr, value in attrs:
            attributes += ' {}="{}"'.format(attr, value)
        self.html.append('  ' * self.indent_level + '<' + tag + attributes + '>')
        self.indent_level += 1

    def handle_endtag(self, tag):
        self.indent_level -= 1
        self.html.append('  ' * self.indent_level + '</' + tag + '>')

    def handle_data(self, data):
        data = data.strip()
        if data:
            self.html.append('  ' * self.indent_level + data)

    def get_formatted_html(self):
        return '\n'.join(self.html)


def file_to_html(filepath, prefix=""):
    parser = Parser(prefix)
    with open(filepath, 'r') as f:
        content = f.read()

    html = parser.parse_content(content)

    formatter = HTMLFormatter()
    formatter.feed(html)
    prettified_html = formatter.get_formatted_html()

    return prettified_html

# Usage
output = file_to_html(filepath, prefix="prefix_")
print(output)
