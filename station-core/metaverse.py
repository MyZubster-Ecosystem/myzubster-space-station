from datetime import datetime
import hashlib
import uuid

spaces = {}
inventories = {}
balances = {}
ledger = []
metaverse_missions = {}


def _now():
    return datetime.utcnow().isoformat()


def _hash(*parts):
    return hashlib.sha256(":".join(str(p) for p in parts).encode()).hexdigest()


def create_space(data):
    space_id = data.get("space_id") or str(uuid.uuid4())
    owner_id = data.get("owner_id")
    if not owner_id:
        raise ValueError("owner_id is required")
    space = {
        "space_id": space_id,
        "name": data.get("name", "Station Compartment"),
        "template": data.get("template", "PERSONAL_HOME"),
        "owner_id": owner_id,
        "access_policy": data.get("access_policy", "PUBLIC"),
        "max_occupancy": data.get("max_occupancy", 50),
        "placed_objects": [],
        "created_at": _now(),
    }
    spaces[space_id] = space
    return space


def add_inventory_item(identity_id, data):
    item_id = data.get("item_id") or str(uuid.uuid4())
    acquired_at = _now()
    item = {
        "item_id": item_id,
        "name": data.get("name", "Station Object"),
        "category": data.get("category", "WEARABLE"),
        "slot": data.get("slot", "HEAD"),
        "rarity": data.get("rarity", "COMMON"),
        "is_transferable": data.get("is_transferable", True),
        "source": data.get("source", "STATION_REWARD"),
        "acquired_at": acquired_at,
    }
    item["provenance_hash"] = _hash(identity_id, item_id, item["source"], acquired_at)
    inventories.setdefault(identity_id, {})[item_id] = item
    return item


def transfer_item(from_id, to_id, item_id):
    item = inventories.get(from_id, {}).get(item_id)
    if not item:
        raise ValueError("item not found")
    if not item["is_transferable"]:
        raise ValueError("item is soulbound and non-transferable")
    inventories.setdefault(to_id, {})[item_id] = item
    del inventories[from_id][item_id]
    return {"from_id": from_id, "to_id": to_id, "item_id": item_id, "transferred": True}


def transfer_myz(from_id, to_id, amount):
    amount = float(amount)
    if amount <= 0:
        raise ValueError("amount must be positive")
    balances.setdefault(from_id, 0.0)
    balances.setdefault(to_id, 0.0)
    if balances[from_id] < amount:
        raise ValueError("insufficient MYZ balance")
    balances[from_id] -= amount
    balances[to_id] += amount
    tx = {
        "transaction_id": str(uuid.uuid4()),
        "from_id": from_id,
        "to_id": to_id,
        "amount": amount,
        "currency": "MYZ",
        "timestamp": _now(),
    }
    tx["receipt_hash"] = _hash(tx["transaction_id"], from_id, to_id, amount, tx["timestamp"])
    ledger.append(tx)
    return tx


def create_metaverse_mission(data):
    mission_id = data.get("mission_id") or str(uuid.uuid4())
    mission = {
        "mission_id": mission_id,
        "name": data.get("name", "Station Mission"),
        "participants": data.get("participants", []),
        "status": "CREATED",
        "is_demo_data": bool(data.get("is_demo_data", True)),
        "created_at": _now(),
    }
    metaverse_missions[mission_id] = mission
    return mission
