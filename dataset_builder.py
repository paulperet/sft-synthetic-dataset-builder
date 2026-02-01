import pandas as pd
import os
from openai import OpenAI
import time
import argparse
from pathlib import Path
import os
import filecmp
from concurrent.futures import ThreadPoolExecutor

def collect_data(api_endpoint: str, threads: int, examples: int):
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
    subjects = open("subjects.txt").read().split(";")[:examples]

    def process_query(subject):
        try:
            response = client.chat.completions.create(
            model="deepseek-chat",
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
        executor.map(process_query, subjects)
    
    print("Data collection completed.")

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
        help="Number of threads to use for data collection.",
    )

    parser.add_argument(
        "--examples",
        type=int,
        default=100,
        help="Number of examples to use for data collection.",
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    collect_data(
        api_endpoint=args.api_endpoint,
        threads=args.threads,
        examples=args.examples,
    )