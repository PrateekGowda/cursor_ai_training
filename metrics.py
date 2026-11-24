"""Simulated host metrics (no SSH). Values are deterministic per server id + time bucket."""

from __future__ import annotations

import random
import time
from typing import Any


def simulate_metrics(server_id: int) -> dict[str, Any]:
    """Return CPU, memory, network, and listening ports for a server id."""
    # Refresh window ~5s so the UI sees gentle movement without being random noise.
    bucket = int(time.time() // 5)
    rng = random.Random(f"{server_id}:{bucket}")

    mem_total_gib = rng.choice([8, 16, 32, 64])
    mem_used_gib = round(rng.uniform(mem_total_gib * 0.25, mem_total_gib * 0.85), 1)

    base_ports = [22, 80, 443]
    extra = [p for p in (3000, 5001, 5432, 6379, 8080, 9100) if rng.random() > 0.55]
    ports = sorted(set(base_ports + extra))

    return {
        "server_id": server_id,
        "cpu_percent": round(rng.uniform(5, 92), 1),
        "memory": {
            "used_gib": mem_used_gib,
            "total_gib": mem_total_gib,
        },
        "network": {
            "in_mbps": round(rng.uniform(0.1, 85.0), 1),
            "out_mbps": round(rng.uniform(0.1, 60.0), 1),
        },
        "listening_ports": ports,
        "simulated": True,
    }
