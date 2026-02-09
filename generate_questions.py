import pandas as pd
import os
from openai import OpenAI
from pathlib import Path
import os
from concurrent.futures import ThreadPoolExecutor
import yaml

def generate_questions():
    API_KEY = os.getenv("LLM_API_KEY")

    with open('data.yaml', 'r') as file:
        loaded_data = yaml.safe_load(file)
        api_endpoint = loaded_data.get('api-endpoint', api_endpoint)
        model = loaded_data.get('model', model)
        threads = loaded_data.get('threads', threads)
        examples = loaded_data.get('examples', examples)

    client = OpenAI(api_key=API_KEY, base_url=api_endpoint)

    # Add custom instructions and output format
    custom_instruction = open("instruction_prompt.txt").read()
    
    folder = "questions"
    Path(folder).mkdir(parents=True, exist_ok=True)

    # Use a list of different subjects to create a diverse dataset
    subjects = open("subjects.txt").read().split(";")[:examples]

    def process_query(subject):
        try:
            response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": custom_instruction},
                {"role": "user", "content": f"You will base the query on the subject: {subject}"},
            ],
            stream=False
                    )

            with open(os.path.join(folder, subject+".txt"), "w") as f:
                output = response.choices[0].message.content
                f.write(output)

            print(f"Processed {subject} successfully.")
        except Exception as e:
            print(f"Error processing {subject}: {e}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(process_query, subjects)
    
    print("Question generation completed.")

if __name__ == "__main__":
    generate_questions()