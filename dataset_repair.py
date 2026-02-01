import pandas as pd
import os
from openai import OpenAI
import time
import argparse
from pathlib import Path
import os
import filecmp
from concurrent.futures import ThreadPoolExecutor
from transformers import AutoTokenizer
import json

tokenizer = AutoTokenizer.from_pretrained("openai/gpt-oss-20b")

def repair_data(api_endpoint: str, threads: int, model: str):
    API_KEY = os.getenv("LLM_API_KEY")

    client = OpenAI(api_key=API_KEY, base_url=api_endpoint)

    prompt_instruct = """
    Return JSON format only:

    [
        {"messages": [
            {
                "role": "user",
                "content": "### Problem statement :\n problem statement and answer\n ### Student question :\n Can you explain me X?"
            },
            {
                "role": "assistant",
                "thinking": "reasoning steps here",
                "content": "guidance and feedback here"
            },
        ]
    ]

    Text:
    {text}
    """

    # Add custom instructions and output format
    custom_instructions = open("instruction_prompt.txt").read()
    prompt_instruct += "\n" + custom_instructions + "\n"

    folder = "output"
    Path(folder).mkdir(parents=True, exist_ok=True)

    # Use a list of different subjects to create a diverse dataset
    # Test incorrect json files

    incorrect_files = []

    for file in os.listdir("output"):
        if not file.endswith(".json"):
            continue
        try:
            messages = json.loads(open(os.path.join("output", file)).read())[0]["messages"]
            conversation = tokenizer.apply_chat_template(messages, tokenize=False)
        except Exception as e:
            incorrect_files.append(file)

    print("Number of incorrect files:", len(incorrect_files))
    if len(incorrect_files) == 0:
        print("No incorrect files found. You are done!")
        return

    for file in incorrect_files:
        os.remove(os.path.join("output", file))

    incorrect_files = [file_name.strip(".json") for file_name in incorrect_files]

    def process_query(subject):
        try:
            response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt_instruct},
                {"role": "user", "content": f"You will base the query on the subject: {subject}"},
            ],
            stream=False
                    )

            with open(os.path.join(folder, subject+".json"), "w") as f:
                output = response.choices[0].message.content
                if output.startswith("```json"):
                    output = output.strip("```").strip()
                    if output.startswith("json"):
                        output = output[4:].strip()
                f.write(output)

            print(f"Processed {subject} successfully.")
        except Exception as e:
            print(f"Error processing {subject}: {e}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(process_query, incorrect_files)
    
    print("Data repair completed.")

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--api-endpoint",
        type=str,
        default="https://api.deepseek.com",
        help="Path to your favorite API endpoint.",
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=50,
        help="Number of threads to use for data repair.",
    )

    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model to use for data repair. example: deepseek-chat",
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    repair_data(
        api_endpoint=args.api_endpoint,
        threads=args.threads,
        model=args.model,
    )