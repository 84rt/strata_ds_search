# Backend Directory

This directory contains scripts and notebooks for downloading, saving and hashing datasets used later keyword search.

## Data Storage

The data on which the keyword search is going to be performed should be stored in `backend/data/` 

## Conda Environment

A Conda environment is set up in the home folder to manage dependencies for this project. To activate the environment, use the following command:

```bash
conda activate /path/to/your/conda/environment
```

Ensure that you have all the necessary packages installed as specified in your environment configuration file (e.g., `environment.yml`).

## Downloading Test Datasets

To download the test datasets, you need to have the `datasets` library installed. You can install it using pip:

```bash
pip install datasets
```

Once installed, you can use the `datasets_main.ipynb` notebook to download the datasets. This notebook includes functionality to load datasets from the `data` directory, create Merkle tree hashes for each dataset, and save these hashes to a JSON file for integrity verification.

## Dataset Sizes

This project uses subsets of the following datasets from Hugging Face:

- **Wikipedia (English)**: ~31.96 GB total (includes downloaded and generated data).  
  [Source](https://huggingface.co/datasets/legacy-datasets/wikipedia)

- **BookCorpus**: ~6.03 GB total.  
  [Source](https://huggingface.co/datasets/bookcorpus/bookcorpus)

> **Note**: Sizes may vary based on preprocessing.

## Dataset Hashing

The `datasets_main.ipynb` notebook includes functionality to load datasets from the `data` directory, create Merkle tree hashes for each dataset, and save these hashes to a JSON file for integrity verification.

## Directory Structure

- `datasets_main.ipynb`: Jupyter notebook for downloading, processing, and hashing datasets.
- `data/`: Directory where datasets are stored.

Ensure that the `data/` directory exists and is properly structured to store the datasets as expected by the scripts and notebooks.



### Current sizes of downloaded datasets
- bookcorpus: **1020K**
- tiny_shakespeare: **249M**
- wikipedia_dataset: **5G**


---

TOOD (assure) later:
- Make sure that the dataset is processed in the same way (this is to assure that the resoulting hash is the same, even if the dataset is processed, compressed or stored in a different way)
    - white-spaces removed
    - same file format 
    - use the same hashing function: **SHA-256**
    - use the same chunking size: **64MB**