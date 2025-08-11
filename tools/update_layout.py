import json

with open("solar_microgrid_sim/data/sample_layout.json") as f:
    layout = json.load(f)

for node in layout["nodes"]:
    node["battery_capacity"] = 20
    node["stored_energy"] = 0

with open("solar_microgrid_sim/data/sample_layout.json", "w") as f:
    json.dump(layout, f, indent=2)
