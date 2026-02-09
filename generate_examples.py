import os
from openai import OpenAI
from pathlib import Path
import os
from concurrent.futures import ThreadPoolExecutor
import yaml
import json

def generate_examples():
    API_KEY = os.getenv("LLM_API_KEY")

    with open('config.yaml', 'r') as file:
        loaded_data = yaml.safe_load(file)
        api_endpoint = loaded_data.get('api-endpoint')
        model = loaded_data.get('model')
        threads = loaded_data.get('threads')
        thinking = loaded_data.get('thinking')

    client = OpenAI(api_key=API_KEY, base_url=api_endpoint)

    # Add system instructions
    custom_instruction = open("system_prompt.txt").read()
    
    folder = "examples"
    Path(folder).mkdir(parents=True, exist_ok=True)

    # Use a list of different subjects to create a diverse dataset
    questions = os.listdir("questions")

    def process_query(question):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                        {"role": "system", "content": custom_instruction},
                        {"role": "user", "content": open(os.path.join("questions", question)).read()}
                    ],
                reasoning_effort="high",
                temperature=0.2,
                stream=False
            )

            
            cot_trace = response.choices[0].message.reasoning_content
            final_answer = response.choices[0].message.content

            if thinking:
                structure = [
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": open(os.path.join("questions", question)).read()
                            },
                            {
                                "role": "assistant",
                                "thinking": cot_trace,
                                "content": final_answer
                            }
                        ]
                    }
                ]
            else:
                structure = [
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": open(os.path.join("questions", question)).read()
                            },
                            {
                                "role": "assistant",
                                "content": final_answer
                            }
                        ]
                    }
                ]
            

            with open(os.path.join("examples", question.strip(".txt")+".json"), "w") as f:
                json.dump(structure, f, indent=4)

            print(f"Processed {question} successfully.")
        except Exception as e:
            print(f"Error processing {question}: {e}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(process_query, questions)
    
    print("Question generation completed.")

if __name__ == "__main__":
    generate_examples()