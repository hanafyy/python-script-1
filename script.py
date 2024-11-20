import os
import requests

# Set up directory paths
source_directory = './'
summary_directory = './summaries'

# Ensure the summary directory exists
if not os.path.exists(summary_directory):
    os.makedirs(summary_directory)

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
headers = {"Authorization": "Bearer token"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Process each text file in the directory
for filename in os.listdir(source_directory):
    if filename.endswith('.txt'):  # Check if the file is a text file
        file_path = os.path.join(source_directory, filename)
        summary_path = os.path.join(summary_directory, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            output = query({
                "inputs": content,
                "parameters": {"max_length": 150},
                "options": {"use_cache": False, "wait_for_model": True}
            })
          
            # Extract the summarized text from the output
            summarized_text = output[0]['generated_text']

        # Write or update the summary file
        with open(summary_path, 'w', encoding='utf-8') as summary_file:
            summary_file.write(summarized_text)
        print(f"Processed and saved summary for {filename}")
