import hashlib
import json
import os
from typing import List

from datasets import load_dataset
from huggingface_hub import list_datasets
from tqdm import tqdm
from datasets import load_dataset, Dataset

import time
import os
import json
from datasets import load_dataset
from tqdm import tqdm  # For progress tracking
import jsonlines  # Optional: Install using `pip install jsonlines`

def download_and_save_dataset(dataset_name, subset=None, batch_size=1000):


# ... existing code ...

    # Load the dataset in streaming mode with retry mechanism
    max_retries = 20
    retry_delay = 5  # initial delay in seconds

    for attempt in range(max_retries):
        try:
            dataset = load_dataset(dataset_name, split='train', streaming=True)
            break
        except ConnectionError as e:
            print(f"Got disconnected from remote data host. Retrying in {retry_delay}sec [{attempt + 1}/{max_retries}]")
            time.sleep(retry_delay)
            retry_delay *= 2  # exponential backoff
    else:
        raise ConnectionError("Failed to connect to the server after multiple attempts.")

# ... existing code ...

    # Load the dataset
    if subset:
        dataset = load_dataset(dataset_name, subset=subset, split='train', streaming=True)
    else:
        dataset = load_dataset(dataset_name, split='train', streaming=True)

    # Specify the save file
    save_file = f"./data/{dataset_name}_dataset.jsonl"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_file), exist_ok=True)

    # Open the file in append mode
    with jsonlines.open(save_file, mode='a') as writer:
        batch = []
        try:
            for example in tqdm(dataset, desc=f"Downloading {dataset_name}"):
                batch.append(example)
                if len(batch) == batch_size:
                    # Write the batch to the file
                    writer.write_all(batch)
                    batch = []  # Clear the batch

            # Write any remaining examples in the last batch
            if batch:
                writer.write_all(batch)

            print(f"Dataset successfully saved to {save_file}")

        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Progress saved up to this point. You can restart the script to continue.")

# Example usage
download_and_save_dataset('huggingface_dataset_name', subset='subset_name', batch_size=1000)



# List of datasets with size information in comments
"""
Dataset Descriptions:
- tiny_shakespeare (~450 KB): A very small dataset ideal for testing or experimentation.
- bookcorpus (~6 GB): Text extracted from books, used in LLM pretraining.
- wikipedia (subset: 20220301.en, ~16 GB): English Wikipedia dump as of March 2022.
- openwebtext (~40 GB): Open-source recreation of the WebText dataset.
- the_pile (~825 GB): A massive dataset designed for large language model training.
- c4 (subset: en, ~750 GB): Cleaned version of Common Crawl, frequently used for large-scale LLM training.
- oscar (subset: unshuffled_deduplicated_en, ~1.3 TB): A multilingual web corpus.
- common_crawl (Several TBs): Raw web crawl data; storage needs depend on the specific subset downloaded.
"""
datasets_to_download = [
    # {"name": "tiny_shakespeare"},  # ~450 KB
    {"name": "bookcorpus"},       # ~6 GB
    # {"name": "wikipedia", "subset": "20220301.en"},  # ~16 GB
    # {"name": "openwebtext"},      # ~40 GB
    # {"name": "the_pile"},         # ~825 GB
    # {"name": "c4", "subset": "en"},  # ~750 GB
    # {"name": "oscar", "subset": "unshuffled_deduplicated_en"},  # ~1.3 TB
    # {"name": "common_crawl"}      # Several TBs
]


# Loop through the datasets and download them
for dataset_info in datasets_to_download:
    name = dataset_info["name"]
    subset = dataset_info.get("subset")  # Subset is optional
    download_and_save_dataset(name, subset)
