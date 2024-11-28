# %%
import json
from datasets import load_dataset

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
ds_to_download = "tiny_shakespeare"

# Load the Wikipedia dataset
dataset = load_dataset(ds_to_download)  # Replace with your desired language/date

# %%
# CHECK IF THE DATASET IS CORRECT

# Access the 'train' split
for example in dataset['train']:
    print(example)
    break  # Print the first example

# %%
# SAVE THE DATASET LOCALLY

dataset.save_to_disk(f"./{ds_to_download}")

# %% 

def hash_content(content: str) -> str:
    """Hash a string using SHA-256"""
    return hashlib.sha256(content.encode()).hexdigest()

def create_merkle_tree(data_list: List[str]) -> str:
    """Create a Merkle tree from a list of data and return root hash"""
    if not data_list:
        return hash_content("")
    
    # Create leaf nodes by hashing each piece of data
    hashes = [hash_content(str(data)) for data in data_list]
    
    # Build tree bottom-up until we reach root
    while len(hashes) > 1:
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])  # Duplicate last hash if odd number
        
        next_level = []
        for i in range(0, len(hashes), 2):
            combined = hashes[i] + hashes[i+1]
            next_level.append(hash_content(combined))
        hashes = next_level
        
    return hashes[0]  # Return root hash

# Load and hash Wikipedia dataset
wiki_data = load_dataset_from_directory(wiki_path)
wiki_hash = create_merkle_tree(wiki_data)
print(f"Wikipedia dataset hash: {wiki_hash}")

# Load and hash BookCorpus dataset
books_data = load_dataset_from_directory(books_path)
books_hash = create_merkle_tree(books_data)
print(f"BookCorpus dataset hash: {books_hash}")

# Save dataset hashes to a JSON file
dataset_hashes = {
    "wikipedia": wiki_hash,
    "bookcorpus": books_hash
}

hash_file_path = os.path.join("data", "dataset_hashes.json")
with open(hash_file_path, "w") as f:
    json.dump(dataset_hashes, f, indent=4)

print(f"Dataset hashes saved to: {hash_file_path}")



# %%