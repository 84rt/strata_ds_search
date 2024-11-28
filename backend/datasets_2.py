# %%
from datasets import load_dataset

# Load the Wikipedia dataset
dataset = load_dataset("tiny_shakespeare")  # Replace with your desired language/date

# %%
# Access the 'train' split
for example in dataset['train']:
    print(example)
    break  # Print the first example
# %%

dataset.save_to_disk("./tiny_shakespeare")

# %%