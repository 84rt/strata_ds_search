import pandas as pd
from datasets import load_dataset
import os

# Define the dataset name
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

dataset_name = 'bookcorpus'

# Load the dataset in streaming mode
dataset = load_dataset(dataset_name, split='train', streaming=True)

# Define batch size for saving data
batch_size = 100000
batch = []
file_index = 0

# Ensure the directory for the specific dataset exists
os.makedirs(f'backend/data/{dataset_name}', exist_ok=True)

# Iterate over the dataset and save in batches with simple progress display
print(f"Starting download and processing of {dataset_name}...")
for i, example in enumerate(dataset):
    batch.append(example)
    if (i + 1) % batch_size == 0:
        df = pd.DataFrame(batch)
        df.to_csv(f'backend/data/{dataset_name}/{dataset_name}_part_{file_index}.csv', index=False)
        batch = []
        file_index += 1
        print(f"Processed {i + 1} examples...")

# Save any remaining data
if batch:
    df = pd.DataFrame(batch)
    df.to_csv(f'backend/data/{dataset_name}/{dataset_name}_part_{file_index}.csv', index=False)

print(f"Download and processing of {dataset_name} completed.")
