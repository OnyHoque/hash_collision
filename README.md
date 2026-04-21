# Hash Function Collision Analyzer

A Python project for testing and comparing custom string hash functions in a hash table setting.

This project loads a large dataset of words, runs each hash function against the same input, and measures how evenly the words are distributed across a fixed-size hash table. The goal is to compare collision behavior and identify which hashing strategies perform best for this dataset.

---

## Project Overview

In this project, multiple hash functions are stored in a `hash_functions/` folder. Each script inside that folder defines the same function:

```python
def hash_string(s):
    ...