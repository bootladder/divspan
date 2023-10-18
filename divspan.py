#!/usr/bin/python
from html.parser import HTMLParser
import re
import sys
import argparse

class HTMLFormatter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.indent_level = 0
        self.formatted_html = []

    def handle_starttag(self, tag, attrs):
        self.formatted_html.append(f'{"  " * self.indent_level}<{tag}{self.attrs_to_string(attrs)}>')
        self.indent_level += 1

    def handle_endtag(self, tag):
        self.indent_level -= 1
        self.formatted_html.append(f'{"  " * self.indent_level}</{tag}>')

    def handle_data(self, data):
        self.formatted_html.append(f'{"  " * self.indent_level}{data.strip()}')

    def attrs_to_string(self, attrs):
        if not attrs:
            return ''
        return ' ' + ' '.join(f'{k}="{v}"' for k, v in attrs)

    def get_formatted_html(self):
        return '\n'.join(self.formatted_html)

def convert_to_html(input_text, prefix="prefix"):
    lines = input_text.strip().split("\n\n")  # Divided by double newlines
    html_output = []
    div_count = 0
    span_count = 0

    for line in lines:
        div_count += 1
        fragments = line.split("  ")  # Fragments are divided by double spaces
        div_content = []

        # Check for a custom class in the div definition
        div_class_hint = fragments[0].split("#")
        if len(div_class_hint) > 1:
            div_class = div_class_hint[1].split()[0]  # Get only the class name
            fragments[0] = fragments[0].replace("#" + div_class, "").strip()
        else:
            div_class = f"{prefix}_{div_count}"

        for index, fragment in enumerate(fragments):
            # Check for a custom class in the span definition
            span_class_hint = fragment.split("#")
            if len(span_class_hint) > 1:
                span_class = span_class_hint[1].split()[0]  # Get only the class name
                fragment = fragment.replace("#" + span_class, "").strip()
            else:
                span_count += 1
                span_class = f"{prefix}_{span_count}"

            if 0 < index < len(fragments) - 1:  # Only wrap middle fragments in spans
                div_content.append(f'<span class="{span_class}">{fragment}</span>')
            else:
                div_content.append(fragment)

        html_output.append(f'<div class="{div_class}">{" ".join(div_content)}</div>')

    return '\n'.join(html_output)



def main():
    parser = argparse.ArgumentParser(description="Convert custom syntax to HTML.")
    parser.add_argument("filepath", help="Path to the input file containing custom syntax text.")
    parser.add_argument("-p", "--prefix", default="prefix", help="Prefix for auto-generated class names. Default is 'prefix'.")
    parser.add_argument("-o", "--output", help="Path to save the generated HTML. If not specified, the HTML is printed to console.")

    args = parser.parse_args()

    with open(args.filepath, 'r') as f:
        input_text = f.read()

    result = convert_to_html(input_text, args.prefix)
    formatter = HTMLFormatter()
    formatter.feed(result)

    output_html = formatter.get_formatted_html()

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_html)
    else:
        print(output_html)

if __name__ == "__main__":
    main()
