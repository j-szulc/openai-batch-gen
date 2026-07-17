import argparse
from pathlib import Path
import json
import sys

from openai_batch_gen.basic_gen import BasicGen

DESCRIPTION = "Generate OpenAI batch request"
def get_parser(parser = argparse.ArgumentParser(description=DESCRIPTION)):
    parser.add_argument("--model", type=str, required=True, help="Model to use, e.g. 'gpt-4o'")
    parser.add_argument("--system", type=str, required=True, help="System prompt")
    parser.add_argument("file", type=str, help="JSONL file to read user messages from")
    return parser
    
def main(args = None):
    if args is None:
        parser = get_parser()
        args = parser.parse_args()
    user_messages = [json.loads(line.strip()) for line in Path(args.file).read_text().splitlines()]
    gen = BasicGen(args.model, args.system)
    requests = gen.generate(user_messages)
    for request in requests:
        print(request.model_dump_json(exclude_none=True))

    # stats
    total_system_chars = sum(len(request.body.messages[0].content) for request in requests)
    total_user_chars = sum(len(request.body.messages[1].content) for request in requests)
    total_chars = total_system_chars + total_user_chars
    print(f"Total system chars: {total_system_chars} ({total_system_chars / total_chars * 100:.2f}%)", file=sys.stderr)
    print(f"Total user chars: {total_user_chars} ({total_user_chars / total_chars * 100:.2f}%)", file=sys.stderr)
    CHARS_PER_TOKEN_EST = 4
    print(f"Total tokens assuming {CHARS_PER_TOKEN_EST} chars per token: {total_chars / CHARS_PER_TOKEN_EST}", file=sys.stderr)
    TOKENS_PER_SECOND_EST = 100
    print(f"Total estimated time to complete assuming {TOKENS_PER_SECOND_EST} tokens/sec: {total_chars / TOKENS_PER_SECOND_EST / 60:.0f} minutes", file=sys.stderr)