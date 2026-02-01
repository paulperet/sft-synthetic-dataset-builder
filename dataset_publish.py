import json
import os
import pandas as pd
import os
from datasets import load_dataset
from pathlib import Path
import argparse

def publish_dataset(hf_path: str, private=False):

    hf_token = os.environ["HF_TOKEN"]
    
    data_list = []

    for file in os.listdir("output"):
        if not file.endswith(".json"):
            continue
        try:
            with open(os.path.join("output", file), 'r') as f:
                content = json.load(f)
                # Assuming the structure is a list of dicts, and you want the first one
                messages = content[0]["messages"]
                data_list.append({"messages": messages})
        except Exception as e:
            print(f"Error processing {file}: {e}")

    # Convert to DataFrame and save as JSONL
    df = pd.DataFrame(data_list)
    df.to_json("output/dataset.jsonl", orient="records", lines=True)

    # Load into datasets
    from datasets import load_dataset
    dataset = load_dataset("json", data_files="dataset.jsonl")

    dataset.push_to_hub(hf_path, private=private, token=hf_token)

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--private",
        type=bool,
        default=False,
        help="Whether the dataset should be private.",
    )

    parser.add_argument(
        "--hf-path",
        type=str,
        required=True,
        help="The Hugging Face dataset path (e.g., username/dataset-name).",
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()

    publish_dataset(
        hf_path=args.hf_path,
        private=args.private,
    )
    
