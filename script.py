import json

with open("api-reference/openapi.json", "r") as f:
    data = json.load(f)

# Reorder paths (Health, v2, v1)
new_paths = {}
for k, v in data["paths"].items():
    if "/health" in k:
        new_paths[k] = v

for k, v in data["paths"].items():
    if "/v2/" in k:
        new_paths[k] = v

for k, v in data["paths"].items():
    if "/v1/" in k:
        new_paths[k] = v

data["paths"] = new_paths

# Reorder tags (Health, v2, v1)
new_tags = []
for t in data["tags"]:
    if t["name"] == "Health":
        new_tags.append(t)
for t in data["tags"]:
    if "v2" in t["name"]:
        new_tags.append(t)
for t in data["tags"]:
    if "v1" in t["name"] or "Legacy" in t["name"]:
        new_tags.append(t)

# Add "x-mint" extension to the Legacy v1 API tag to see if we can make it collapsed
for t in new_tags:
    if "Legacy v1 API" in t["name"]:
        t["x-mint"] = {"expanded": False}

# Reorder and define x-tagGroups to make Legacy API collapsed
data["x-tagGroups"] = [
    {"name": "System", "tags": ["Health"]},
    {"name": "API v2", "tags": ["v2 - Markets", "v2 - Snapshots"]},
    {
        "name": "Legacy v1 API",
        "tags": ["Legacy v1 API", "v1 - Markets", "v1 - Snapshots"],
        "x-mintlify": {"expanded": False},
        "x-mint": {"expanded": False},
    },
]

with open("api-reference/openapi.json", "w") as f:
    json.dump(data, f, indent=4)
