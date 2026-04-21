import csv
import os
import importlib

TABLE_SIZE = 1_000_000
FOLDER = "hash_functions"


hash_functions = {}

for filename in os.listdir(FOLDER):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module = importlib.import_module(f"{FOLDER}.{module_name}")

        if hasattr(module, "hash_string"):
            hash_functions[module_name] = module.hash_string
        else:
            print(f"Warning: {filename} does not contain hash_string(s)")

# ----------------------------
# Read all words once
# ----------------------------
data = []
with open("data/unigram_freq.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        word = row["word"]
        count = int(row["count"])
        data.append((word, count))

# ----------------------------
# Evaluate each hash function
# ----------------------------
results = []

for name, func in hash_functions.items():
    bucket_counts = [0] * TABLE_SIZE

    for word, count in data:
        index = func(word) % TABLE_SIZE
        bucket_counts[index] += 1

    num_words = sum(bucket_counts)
    used_buckets = sum(1 for x in bucket_counts if x > 0)
    collisions = sum(x - 1 for x in bucket_counts if x > 1)
    max_bucket_size = max(bucket_counts)
    load_factor = num_words / TABLE_SIZE

    results.append({
        "Algorithm": name,
        "Words": num_words,
        "Used Buckets": used_buckets,
        "Collisions": collisions,
        "Max Bucket Size": max_bucket_size,
        "Load Factor": round(load_factor, 4),
    })

# ----------------------------
# Print as table
# ----------------------------
headers = ["Algorithm", "Words", "Used Buckets", "Collisions", "Max Bucket Size", "Load Factor"]

if results:
    col_widths = {}
    for h in headers:
        col_widths[h] = max(len(h), max(len(str(row[h])) for row in results))

    header_line = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
    separator = "-+-".join("-" * col_widths[h] for h in headers)

    print(header_line)
    print(separator)

    for row in results:
        print(" | ".join(f"{str(row[h]):<{col_widths[h]}}" for h in headers))
else:
    print("No hash functions were loaded.")