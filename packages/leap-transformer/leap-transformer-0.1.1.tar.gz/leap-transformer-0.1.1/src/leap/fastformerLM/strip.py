import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

with open(args.filename, 'r') as f:
    nb = json.load(f)

cells = nb["cells"]
for i in range(len(cells)):
    cells[i]["execution_count"] = None
    if cells[i].get("outputs") is not None:
        outputs = cells[i]["outputs"]
        for j in range(len(outputs)):
            if outputs[j].get("execution_count") is not None:
                outputs[j]["execution_count"] = None
        cells[i]["outputs"] = outputs


nb["cells"] = cells

with open(args.filename, 'w') as f:
    json.dump(nb, f)
