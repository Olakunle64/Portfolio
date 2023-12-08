#!/usr/bin/python3

import re

def find_text(text):
    """find a particular text in a message"""
    check_text = re.compile(r'''(\w+)\.(\w+) #Class name and the command
            \((["\'][A-Za-z0-9_-]+["\'])? #id value
            (,\s["\']\w+["\'])? #attribute name
            (,\s["\']\w+["\'])?\) #attribute value
            ''', re.VERBOSE)
    ret = check_text.search(text)
    print(ret.group(0))
    print(ret.group(1))
    print(ret.group(2))
    print(ret.group(3))
    print(ret.group(4))
    print(ret.group(5))

def find_text2(text):
    """find a particular text in a message"""
    check_text = re.compile(r'''(\w+)\.(\w+) #Class name and the command
            \((["\'][A-Za-z0-9_-]+["\'])? #id value
            ,\s({ #Opening parenthesis
            [\'"]\w+[\'"]:\s["]?\w+["]? #first key/value pair
            (,\s[\'"]\w+[\'"]:\s["]?\w+["]?)* #first key/value pair
            })\) # closing curly braces
            ''', re.VERBOSE)
    ret = check_text.search(text)
    print(ret.group(0))
    print(ret.group(1))
    print(ret.group(2))
    print(ret.group(3))
    print(ret.group(4))
    """print(ret.group(5))
    print(ret.group(6))
    print(ret.group(7))
    print(ret.group(8))
    print(ret)"""


if __name__ == "__main__":
    my_text = "I love User.show(\"38f2-275\")"
    find_text(my_text)
    print()
    print("--------------------------------------------")
    my_text = "User.update(\"38f22813-2753-4d42-b37c-57a17f1e4f88\", \"John\") user.,update(dklf"
    find_text(my_text)
    my_text = "Is it truly a match User.update(\"38f22813-2753-4d42-b37c-57a17f1e4f88\", {'first_name': \"John\", \"age\": 89, \"gpa\": 40})"
    print()
    print("-------------------------------------------")
    find_text2(my_text)

