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


# GENERATE A HASH OF A DATASET
# load the json file from /data/[dataset_name]/[dataset_name]_sample_0.json
# generate a Merkle tree of the dataset 
# save the root hash to /data/hashes/[dataset_name]_hash
from pymerkle import InmemoryTree as MerkleTree

dataset_name = "tiny_shakespeare"
# dataset_name = "wikipedia_dataset"

# Initialize the Merkle Tree
tree = MerkleTree(hash_type='sha256')

# Load the JSON file
with open(f'./data/{dataset_name}/{dataset_name}_sample_0.json', 'r') as file:
    data = json.load(file)

# Process each entry in the JSON data
for entry in data:
    # Convert each entry to a string and encode it to bytes
    data_chunk = json.dumps(entry).encode('utf-8')
    tree.append_entry(data_chunk)

# Retrieve the root hash after processing all entries
root_hash = tree.get_state().hex()  # Convert bytes to a hex string
print(f"Root Hash: {root_hash}")

# Save the root hash to a file
with open(f'./data/hashes/{dataset_name}_hash', 'w') as hash_file:
    hash_file.write(root_hash)


# %%