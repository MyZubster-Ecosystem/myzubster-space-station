import unittest

from metaverse import (
    spaces, inventories, balances, ledger, metaverse_missions,
    create_space, add_inventory_item, transfer_item, transfer_myz,
    create_metaverse_mission,
)

class MetaverseCoreTests(unittest.TestCase):
    def setUp(self):
        spaces.clear(); inventories.clear(); balances.clear(); ledger.clear(); metaverse_missions.clear()

    def test_spaces(self):
        space = create_space({"space_id": "ROOM_A", "owner_id": "alice", "access_policy": "PRIVATE_OWNER"})
        self.assertEqual(space["owner_id"], "alice")

    def test_inventory_and_soulbound(self):
        wearable = add_inventory_item("alice", {"item_id": "visor", "slot": "HEAD"})
        self.assertEqual(len(wearable["provenance_hash"]), 64)
        badge = add_inventory_item("alice", {"item_id": "badge", "is_transferable": False})
        with self.assertRaises(ValueError): transfer_item("alice", "bob", badge["item_id"])
        self.assertTrue(transfer_item("alice", "bob", wearable["item_id"])["transferred"])

    def test_economy(self):
        balances["alice"] = 100
        tx = transfer_myz("alice", "bob", 25)
        self.assertEqual(balances["alice"], 75)
        self.assertEqual(balances["bob"], 25)
        self.assertEqual(len(tx["receipt_hash"]), 64)

    def test_missions_demo_boundary(self):
        mission = create_metaverse_mission({"mission_id": "M1", "participants": ["alice"]})
        self.assertTrue(mission["is_demo_data"])

if __name__ == "__main__": unittest.main()
