import argparse
from pathlib import Path
import json

from openai_batch_gen.basic_gen import BasicGen

def main():
    parser = argparse.ArgumentParser(description="Generate OpenAI batch request")
    parser.add_argument("--model", type=str, required=True, help="Model to use, e.g. 'gpt-4o'")
    parser.add_argument("--system", type=str, required=True, help="System prompt")
    parser.add_argument("file", type=str, help="JSONL file to read user messages from")
    args = parser.parse_args()

    user_messages = [json.loads(line.strip()) for line in Path(args.file).read_text().splitlines()]
    gen = BasicGen(args.model, args.system)
    requests = gen.generate(user_messages)
    for request in requests:
        print(request.model_dump_json(exclude_none=True))
