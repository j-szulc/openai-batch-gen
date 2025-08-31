#!/usr/bin/env python3
"""
OpenAI Batch Generation CLI

This module provides a command-line interface for generating OpenAI batch requests
and parsing batch responses.
"""

import argparse
import sys
from pathlib import Path

from .request import main as request_main, get_parser as request_parser
from .response import main as response_main, get_parser as response_parser
from .utils import main as utils_main, get_parser as utils_parser

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="OpenAI Batch CLI")

    subparsers = parser.add_subparsers(help="Subcommand", dest="command")
    request_parser(subparsers.add_parser("request"))
    response_parser(subparsers.add_parser("response"))
    utils_parser(subparsers.add_parser("utils"))
    args = parser.parse_args()

    # If no command is provided, show help
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    {
        "request": request_main,
        "response": response_main,
        "utils": utils_main,
    }[args.command](args)
    


if __name__ == "__main__":
    main()
