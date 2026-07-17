import argparse
from pathlib import Path
import json


DESCRIPTION = "Utility functions for OpenAI batch generation"
def get_parser(parser = argparse.ArgumentParser(description=DESCRIPTION)):
    parser.add_argument("files", type=str, nargs="+", help="Files to turn into a single jsonl file")
    return parser
    
def main(args = None):
    if args is None:
        parser = get_parser()
        args = parser.parse_args()
    for file in args.files:
        p = Path(file)
        print(json.dumps(f"{p.name}:\n{p.read_text()}"))