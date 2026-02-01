# Synthetic data generation for LLM supervised fine-tuning

### Installation & Setup

Python 3.x should work (I used 3.14)

First let's install the repository and the python packages:
```bash
python -m venv .venv
pip install -r requirements
```

Secondly, let's create two files:
```bash
touch instruction_prompt.txt
touch subjects.txt
```
Example:

instruction_prompt.txt - You want to explain the role and persona of the assistant
```markdown
You are a software engineer specialized in C, you will generate a question from a user in plain text
and only output the resulting C code. You will also provide reasoning steps.
```

subjects.txt - You want to have multiple examples so the generated dataset contains a lot of diversity. You can create this list by your own or generate it using a LLM.
```markdown
Selection Sort;Bubble Sort;Insertion Sort;Merge Sort;Quick Sort;Heap Sort;Cycle Sort;3-way Merge Sort
```

The "instruction_prompt.txt" file should contain your custom prompt. Depending on your goal you can ask the AI to only output code for example, to create a text to SQL specialized model,
but it can also be a description of a custom persona that you want the AI to adopt.
In subjects.txt you define a list of diverse subjects separated by commas. This is important as it will allow generating a lot of diverse examples which is crucial for LLM fine-tuning.

Thirdly export your API keys that will be used to generate the dataset and publish it on HuggingFace:
```bash
export HF_TOKEN="your_huggingface_token"
export LLM_API_KEY="your_LLM_API_key"
```

### Usage

The first step is to run the dataset builder, providing the api endpoint (ex: https://api.deepseek.com) and model (ex: deepseek-chat), number of threads for concurrent calls and the size of the dataset.
```bash
dataset_builder.py [-h] --api-endpoint API_ENDPOINT [--threads THREADS] [--examples EXAMPLES] --model MODEL
```

Then, you should run this script as long as you have invalid examples as it will check if the JSON files are correctly structured.
```bash
dataset_repair.py [-h] [--api-endpoint API_ENDPOINT] [--threads THREADS] --model MODEL
```

Finally, when there are no incorrect files anymore you can publish your dataset to huggingface providing your repository (ex: john/mydataset)
```bash
dataset_publish.py [-h] [--private PRIVATE] --hf-path HF_PATH
```
