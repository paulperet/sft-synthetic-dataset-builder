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
touch subject.txt
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

The first step is to run the dataset builder, providing the api endpoint (ex: https://api.deepseek.com), number of threads for concurrent calls and the size of the dataset.
```bash
dataset_builder.py [-h] --api-endpoint API_ENDPOINT [--threads THREADS] [--examples EXAMPLES]
```

Then, you should run this script as long as you have invalid examples as it will attempt to apply a template from a tokenizer and find incorrect formats.
```bash
dataset_repair.py [-h] [--api-endpoint API_ENDPOINT] [--threads THREADS] --model MODEL
```

Finally, when there are no incorrect files anymore you can publish your dataset to huggingface providing your repository (ex: john/mydataset)
```bash
dataset_publish.py [-h] [--private PRIVATE] --hf-path HF_PATH
```
