# config.py

UMBRELLA_TYPES = {
    "Foldable": {"area": 5, "efficiency": 0.15},
    "Fixed": {"area": 10, "efficiency": 0.18},
    "Pod": {"area": 12, "efficiency": 0.20, "battery": 5}
}

NODE_ROLES = {
    "EV Oasis": {"demand": 20},
    "Mobility Hub": {"demand": 15},
    "Climate Pod": {"demand": 10},
    "Energy Backbone": {"demand": 25},
    "VPP Peer": {"demand": 5}
}
