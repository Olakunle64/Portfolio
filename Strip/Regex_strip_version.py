#!/usr/bin/python3
"""This module contains a regex like function that
    works the same way as the strip function"""

import re


def regex_strip(string, options=" "):
    strip_regex = re.compile(r'([' + re.escape(options) + '])' + '(.+)\1')
    strip_content = strip_regex.search(string)
    print(strip_content)
    #return strip_content.group(1)

if __name__ == "__main__":
    text = "/kunle/"
    original_text = regex_strip(text, "/")
    print(original_text)


