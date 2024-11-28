# %%
import json
from datasets import load_dataset, load_from_disk
import os

# %%

# LOAD THE DATASET

"""
### LIST OF DATASETS TO CHOSE FROM:
- tiny_shakespeare (~450 KB): A very small dataset ideal for testing or experimentation.
- bookcorpus (~6 GB): Text extracted from books, used in LLM pretraining.
- wikipedia (subset: 20220301.en, ~16 GB): English Wikipedia dump as of March 2022.
- openwebtext (~40 GB): Open-source recreation of the WebText dataset.
- the_pile (~825 GB): A massive dataset designed for large language model training.
- c4 (subset: en, ~750 GB): Cleaned version of Common Crawl, frequently used for large-scale LLM training.
- oscar (subset: unshuffled_deduplicated_en, ~1.3 TB): A multilingual web corpus.
- common_crawl (Several TBs): Raw web crawl data; storage needs depend on the specific subset downloaded.
"""
ds_to_download = "bookcorpus"
local_dataset_path = f"./{ds_to_download}"

# Check if the dataset is already saved locally
if os.path.exists(local_dataset_path):
    # Load the dataset from the local directory
    dataset = load_from_disk(local_dataset_path)
    print(f"Loaded {ds_to_download} from local directory.")
else:
    # Load the dataset from the source
    dataset = load_dataset(ds_to_download)
    print(f"Downloaded {ds_to_download} from source.")

# %%
# CHECK IF THE DATASET IS CORRECT

# Access the 'train' split
for example in dataset['train']:
    print(example)
    break  # Print the first example

# %%
# SAVE THE DATASET LOCALLY

if not os.path.exists(local_dataset_path):
    dataset.save_to_disk(local_dataset_path)
    print(f"Dataset saved to {local_dataset_path}")

# %% 
import hashlib

def hash_function(data):
    return hashlib.sha256(data).hexdigest()

def merkle_tree(chunks):
    current_level = [hash_function(chunk) for chunk in chunks]
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            if i + 1 < len(current_level):
                combined = current_level[i] + current_level[i + 1]
            else:
                combined = current_level[i]  # Handle odd number of hashes
            next_level.append(hash_function(combined.encode()))
        current_level = next_level
    return current_level[0] if current_level else None

def save_merkle_root_to_file(dataset, file_path):
    chunks = [json.dumps(example).encode() for example in dataset['train']]
    merkle_root = merkle_tree(chunks)
    with open(file_path, 'w') as f:
        f.write(merkle_root)
    print(f"Merkle Root saved to {file_path}")

# Use the loaded dataset and save the Merkle root to a file
save_file_path = f"./data/{ds_to_download}_merkle_root.txt"
os.makedirs(os.path.dirname(save_file_path), exist_ok=True)
save_merkle_root_to_file(dataset, save_file_path)

# %%