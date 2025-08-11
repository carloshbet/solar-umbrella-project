import json
from energy_model import distribute_energy

with open("data/test_nodes.json") as f:
    test_nodes = json.load(f)

sunlight_hours = 6
results = distribute_energy(test_nodes, sunlight_hours)

for node_id, data in results.items():
    print(f"{node_id}: {data}")
