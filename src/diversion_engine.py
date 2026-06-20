import math
import networkx as nx


def haversine_km(a, b):
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat, dlon = lat2-lat1, lon2-lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371 * 2 * math.asin(math.sqrt(h))


def build_sample_road_graph(center=(12.9716, 77.5946)):
    lat, lon = center
    nodes = {
        "Event Zone": center,
        "North Corridor": (lat+0.035, lon),
        "South Corridor": (lat-0.035, lon),
        "East Corridor": (lat, lon+0.035),
        "West Corridor": (lat, lon-0.035),
        "Outer Ring Link": (lat+0.025, lon+0.025),
        "Emergency Bypass": (lat-0.025, lon-0.025),
    }
    G = nx.Graph()
    for name, pos in nodes.items():
        G.add_node(name, pos=pos)
    edges = [
        ("North Corridor", "Outer Ring Link"), ("Outer Ring Link", "East Corridor"),
        ("East Corridor", "South Corridor"), ("South Corridor", "Emergency Bypass"),
        ("Emergency Bypass", "West Corridor"), ("West Corridor", "North Corridor"),
        ("North Corridor", "Event Zone"), ("South Corridor", "Event Zone"),
        ("East Corridor", "Event Zone"), ("West Corridor", "Event Zone"),
    ]
    for u, v in edges:
        G.add_edge(u, v, weight=haversine_km(nodes[u], nodes[v]))
    return G


def recommend_diversions(lat, lon, congestion_score):
    G = build_sample_road_graph((float(lat), float(lon)))
    blocked = "Event Zone"
    routes = []
    pairs = [("North Corridor", "South Corridor"), ("West Corridor", "East Corridor"), ("Emergency Bypass", "Outer Ring Link")]
    H = G.copy()
    if congestion_score >= 60 and blocked in H:
        H.remove_node(blocked)
    for src, dst in pairs:
        try:
            path = nx.shortest_path(H, src, dst, weight="weight")
            delay_reduction = max(8, min(35, int(float(congestion_score) / 3)))
            routes.append({"from": src, "to": dst, "route": " → ".join(path), "estimated_delay_reduction_min": delay_reduction})
        except nx.NetworkXNoPath:
            pass
    return routes
