def distribute_energy(nodes, sunlight_hours):
    results = {}
    surplus_pool = []
    deficit_pool = []

    # Phase 1: Local battery adjustment
    for node in nodes:
        node_id = node["id"]
        base_energy = node["base_energy"]
        usage_factor = node["usage_factor"]
        battery_capacity = node.get("battery_capacity", 0)
        stored_energy = node.get("stored_energy", 0)

        # 🌞 Energy generation based on sunlight
        generated = sunlight_hours * 10
        demand = base_energy * usage_factor
        net_energy = generated - demand

        # 🔋 Battery interaction
        if net_energy > 0:
            available_space = battery_capacity - stored_energy
            stored = min(net_energy, available_space)
            stored_energy += stored
            surplus = net_energy - stored
        else:
            needed = abs(net_energy)
            used = min(needed, stored_energy)
            stored_energy -= used
            surplus = net_energy + used

        node["stored_energy"] = stored_energy

        results[node_id] = {
            "umbrella": node.get("umbrella", "Type B"),
            "role": node.get("role", "Consumer"),
            "generated": round(generated, 2),
            "demand": round(demand, 2),
            "surplus": round(surplus, 2),
            "stored_energy": round(stored_energy, 2),
            "battery_capacity": battery_capacity,
            "energy": round(generated, 2)  # 🔧 Added for chart compatibility
        }

        if surplus > 0:
            surplus_pool.append((node_id, surplus))
        elif surplus < 0:
            deficit_pool.append((node_id, abs(surplus)))

    # Phase 2: Peer-to-peer redistribution
    total_surplus = sum(s for _, s in surplus_pool)
    total_deficit = sum(d for _, d in deficit_pool)

    if total_surplus > 0 and total_deficit > 0:
        for deficit_id, deficit_amount in deficit_pool:
            share = deficit_amount / total_deficit
            received = share * total_surplus
            results[deficit_id]["surplus"] += round(received, 2)

        for surplus_id, surplus_amount in surplus_pool:
            share = surplus_amount / total_surplus
            given = share * total_deficit
            results[surplus_id]["surplus"] -= round(given, 2)

    return results
