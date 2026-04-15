import csv
import hashlib

TABLE_SIZE = 10000000

# ----------------------------
# Hash functions
# ----------------------------
def djb2(s):
    h = 5381
    for ch in s:
        h = ((h << 5) + h) + ord(ch)   # h * 33 + ord(ch)
    return h & 0xFFFFFFFFFFFFFFFF


def sdbm(s):
    h = 0
    for ch in s:
        h = ord(ch) + (h << 6) + (h << 16) - h
    return h & 0xFFFFFFFFFFFFFFFF


def fnv1a(s):
    h = 14695981039346656037
    fnv_prime = 1099511628211
    for ch in s:
        h ^= ord(ch)
        h *= fnv_prime
    return h & 0xFFFFFFFFFFFFFFFF


def sha256_hash(s):
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16)


def md5_hash(s):
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16)


hash_functions = {
    "DJB2": djb2,
    "SDBM": sdbm,
    "FNV-1a": fnv1a,
    "SHA-256": sha256_hash,
    "MD5": md5_hash,
}

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

# compute column widths
col_widths = {}
for h in headers:
    col_widths[h] = max(len(h), max(len(str(row[h])) for row in results))

# print header
header_line = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
separator = "-+-".join("-" * col_widths[h] for h in headers)

print(header_line)
print(separator)

# print rows
for row in results:
    print(" | ".join(f"{str(row[h]):<{col_widths[h]}}" for h in headers))