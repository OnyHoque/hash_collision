import csv

TABLE_SIZE = 1000000   # prime number is a good choice

# create empty hash table
hash_table = [[] for _ in range(TABLE_SIZE)]

# simple string hash function: djb2
def djb2(s):
    h = 5381
    for ch in s:
        h = ((h << 5) + h) + ord(ch)   # h * 33 + ord(ch)
    return h & 0xFFFFFFFF

# insert into hash table
with open("data/unigram_freq.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        word = row["word"]
        count = int(row["count"])

        index = djb2(word) % TABLE_SIZE
        hash_table[index].append((word, count))
        
        
num_words = sum(len(bucket) for bucket in hash_table)
used_buckets = sum(1 for bucket in hash_table if len(bucket) > 0)
collisions = sum(len(bucket) - 1 for bucket in hash_table if len(bucket) > 1)

print("Words in table:", num_words)
print("Used buckets:", used_buckets)
print("Collisions:", collisions)