import argparse
from pathlib import Path
import json
import re

from common.jsonl import from_jsonl


DESCRIPTION = "Utility functions for OpenAI batch generation"
def get_parser(parser = argparse.ArgumentParser(description=DESCRIPTION)):
    parser.add_argument("--regex", type=str, required=True, help="Regex to extract the content from")
    parser.add_argument("--regex-group", type=int, default=0, help="Regex group to extract the content from")
    parser.add_argument("file", type=str, help="JSONL file to extract the regex contents")
    return parser
    
def main(args = None):
    if args is None:
        parser = get_parser()
        args = parser.parse_args()

    for line in from_jsonl(Path(args.file).read_text()):
        match = re.search(args.regex, line, flags=re.DOTALL | re.MULTILINE)
        assert match is not None, f"Match not found in line {line}"
        print(json.dumps(match.group(args.regex_group)))
