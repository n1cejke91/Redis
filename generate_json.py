import json
import random
import string

big_data = {
    "string_data": ''.join(random.choices(string.ascii_letters + string.digits, k=1_000_000)),
    "hash_data": {f"field_{i}": ''.join(random.choices(string.ascii_letters, k=50)) for i in range(20000)},
    "zset_data": [[f"member_{i}", random.randint(1, 10000)] for i in range(20000)],
    "list_data": [ ''.join(random.choices(string.ascii_lowercase, k=100)) for _ in range(200000)]
}

with open("big_data.json", "w") as f:
    json.dump(big_data, f)