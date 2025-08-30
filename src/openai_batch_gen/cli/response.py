import argparse
from pathlib import Path
import json
import sys

from openai_batch_gen.schema.response import BatchResponse

def main():
    parser = argparse.ArgumentParser(description="Parse OpenAI batch response")
    parser.add_argument("file", type=str, help="JSONL file to read user messages from")
    args = parser.parse_args()

    responses = [BatchResponse.model_validate_json(line.strip()) for line in Path(args.file).read_text().splitlines()]
    for response in responses:
        content = response.response.body.choices[0].message.content
        print(json.dumps(content))

    total_input_tokens = sum(response.response.body.usage.input_tokens for response in responses)
    total_completion_tokens = sum(response.response.body.usage.completion_tokens for response in responses)
    print(f"Total input tokens: {total_input_tokens}", file=sys.stderr)
    print(f"Total output tokens: {total_completion_tokens}", file=sys.stderr)
    

    