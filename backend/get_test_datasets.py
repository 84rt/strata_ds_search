# import datasets
from datasets import load_dataset
import os
import json

# Download the datasets (wikipedia, bookcorpusopen)
def download_datasets():
    # Create data directory if it doesn't exist
    data_dir = os.path.join("data")
    os.makedirs(data_dir, exist_ok=True)

    # Download and save Wikipedia dataset
    wiki_dataset = load_dataset("wikipedia", "20220301.en", split="train[:100]", trust_remote_code=True)

    wiki_path = os.path.join(data_dir, "wikipedia")
    os.makedirs(wiki_path, exist_ok=True)
    
    for i, article in enumerate(wiki_dataset):
        with open(os.path.join(wiki_path, f"article_{i}.json"), "w") as f:
            json.dump(article, f)

    # Download and save BookCorpus dataset  
    books_dataset = load_dataset("bookcorpusopen", split="train[:100]")
    books_path = os.path.join(data_dir, "bookcorpus")
    os.makedirs(books_path, exist_ok=True)

    for i, book in enumerate(books_dataset):
        with open(os.path.join(books_path, f"book_{i}.json"), "w") as f:
            json.dump(book, f)


if __name__ == "__main__":
    download_datasets()
