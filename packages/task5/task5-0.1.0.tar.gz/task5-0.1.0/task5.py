# import Counter from collection amd argparse
import argparse
from collections import Counter
from functools import lru_cache


@lru_cache(maxsize=100)
def count(string_object):
    lst1 = Counter(string_object)
    return len([x for x in string_object if lst1[x] == 1])


# Driver Code
if name == "main":
    parser = argparse.ArgumentParser(description="Welcome to Unique Symbol Counter. Let's count unique symbols")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--string",
        "--your string",
        action="store_true",
        help="Type your string to count unique symbols"
    )
    group.add_argument(
        "--file",
        "--path_to_text_file",
        action="store_true",
        help="Type path to text file to count unique symbols"
    )