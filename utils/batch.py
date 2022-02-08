import os
import json

def load_batches():
     # load all batches (10)
    batches_dir = "./data/batches"
    batches = list()
    for batch in os.listdir(batches_dir):
        with open(os.path.join(batches_dir, batch)) as batch_json:
            data = json.load(batch_json)
            batches.append(data)
    return batches