import csv
import os
import importlib
import matplotlib.pyplot as plt

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
            print(f"Warning: {filename} does not contain hash_string")

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

data = data[:300_000]

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
    max_bucket_count = max(bucket_counts)
    sparsity = 1 - (used_buckets / TABLE_SIZE)

    results.append({
        "Algorithm": name,
        "Words": num_words,
        "Used Buckets": used_buckets,
        "Collisions": collisions,
        "Count": max_bucket_count,
        "Sparsity": round(sparsity, 4),
    })

results.sort(key=lambda row: row["Collisions"])

# ----------------------------
# Save as PNG table
# ----------------------------
headers = ["Algorithm", "Words", "Used Buckets", "Collisions", "Count", "Sparsity"]

if results:
    table_data = [[row[h] for h in headers] for row in results]

    fig_height = max(2, 0.5 * len(table_data) + 1.5)
    fig, ax = plt.subplots(figsize=(14, fig_height))
    ax.axis("off")

    table = ax.table(
        cellText=table_data,
        colLabels=headers,
        loc="center",
        cellLoc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(16)
    table.scale(1, 2.0)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold")

    output_file = f"hash_results_{TABLE_SIZE}.png"
    plt.tight_layout()
    plt.savefig(output_file, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Saved table figure to {output_file}")
else:
    print("No hash functions were loaded.")