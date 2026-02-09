import os
import json
import re

for file in os.listdir("examples"):
    if not file.endswith(".json"):
        continue
    try:
        with open(os.path.join("examples", file), 'r') as f:
            content = json.load(f)
            # Assuming the structure is a list of dicts, and you want the first one
            cot = content[0]["messages"]["assistant"]["thinking"]

        regex_patterns = [("The system says\s?([a-z])", "\u$1"), ("We need to be mindful of the instruction", "We should"), ("According to the system instructions,\s?([a-z])", "\u$1"), ("The system says:\s?", ""), ("The instruction says", "We should"), ("According to the system instructions", "We should"), ("The policy says", "Our policy says"), ("The system says ", "")]

        for pattern, replacement in regex_patterns:
            cot = re.sub(pattern, replacement, cot)

        with open(os.path.join("examples", file), 'w') as f:
            content[0]["messages"]["assistant"]["thinking"] = cot
            json.dump(content, f, indent=4)
        
    except Exception as e:
        print(f"Error processing {file}: {e}")