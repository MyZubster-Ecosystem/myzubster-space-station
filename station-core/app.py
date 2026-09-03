from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import uuid
import os

from metaverse import (
    spaces, inventories, balances, ledger, metaverse_missions,
    create_space, add_inventory_item, transfer_item, transfer_myz,
    create_metaverse_mission,
)

app = Flask(__name__)
CORS(app)

missions = []
robots = {
    "eva-ioni-001": {
        "robot_id": "eva-ioni-001", "name": "EVA IONI", "status": "online",
        "battery": 87, "location": "green-module", "last_seen": datetime.utcnow().isoformat()
    }
}
telemetry = []
payments = []

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"station": "MYZUBSTER-SPACE-STATION", "status": "online", "timestamp": datetime.utcnow().isoformat(), "version": "0.2.0"})

@app.route("/api/robots", methods=["GET"])
def get_robots(): return jsonify(list(robots.values()))

@app.route("/api/robots/<robot_id>", methods=["GET"])
def get_robot(robot_id):
    if robot_id not in robots: return jsonify({"error": "Robot not found"}), 404
    return jsonify(robots[robot_id])

@app.route("/api/missions", methods=["GET"])
def get_missions(): return jsonify(missions)

@app.route("/api/missions", methods=["POST"])
def create_mission():
    data = request.json or {}
    mission = {"id": str(uuid.uuid4()), "type": data.get("type", "environmental_scan"), "target": data.get("target", "green-module"), "robot_id": data.get("robot_id"), "status": "CREATED", "created_at": datetime.utcnow().isoformat()}
    missions.append(mission)
    return jsonify(mission), 201

@app.route("/api/missions/<mission_id>/complete", methods=["POST"])
def complete_mission(mission_id):
    for mission in missions:
        if mission["id"] == mission_id:
            mission["status"] = "COMPLETED"; mission["completed_at"] = datetime.utcnow().isoformat(); return jsonify(mission)
    return jsonify({"error": "Mission not found"}), 404

@app.route("/api/telemetry", methods=["GET"])
def get_telemetry(): return jsonify(telemetry)

@app.route("/api/telemetry", methods=["POST"])
def add_telemetry():
    data = request.json or {}
    point = {"id": str(uuid.uuid4()), "robot_id": data.get("robot_id"), "timestamp": datetime.utcnow().isoformat(), "temperature": data.get("temperature"), "humidity": data.get("humidity"), "battery": data.get("battery"), "location": data.get("location")}
    telemetry.append(point); return jsonify(point), 201

@app.route("/api/payments", methods=["GET"])
def get_payments(): return jsonify(payments)

@app.route("/api/payments", methods=["POST"])
def create_payment():
    data = request.json or {}
    payment = {"id": str(uuid.uuid4()), "amount": data.get("amount"), "currency": data.get("currency", "MYZ"), "purpose": data.get("purpose", "Mission payment"), "status": "COMPLETED", "timestamp": datetime.utcnow().isoformat(), "transaction_id": str(uuid.uuid4())[:8]}
    payments.append(payment); return jsonify(payment), 201

@app.route("/api/metaverse/spaces", methods=["GET", "POST"])
def metaverse_spaces_api():
    if request.method == "GET": return jsonify(list(spaces.values()))
    try: return jsonify(create_space(request.json or {})), 201
    except ValueError as exc: return jsonify({"error": str(exc)}), 400

@app.route("/api/metaverse/inventory/<identity_id>", methods=["GET", "POST"])
def metaverse_inventory_api(identity_id):
    if request.method == "GET": return jsonify(list(inventories.get(identity_id, {}).values()))
    return jsonify(add_inventory_item(identity_id, request.json or {})), 201

@app.route("/api/metaverse/inventory/transfer", methods=["POST"])
def metaverse_inventory_transfer_api():
    data = request.json or {}
    try: return jsonify(transfer_item(data.get("from_id"), data.get("to_id"), data.get("item_id")))
    except ValueError as exc: return jsonify({"error": str(exc)}), 400

@app.route("/api/metaverse/economy/<identity_id>", methods=["GET"])
def metaverse_balance_api(identity_id): return jsonify({"identity_id": identity_id, "balance": balances.get(identity_id, 0.0), "currency": "MYZ"})

@app.route("/api/metaverse/economy/transfer", methods=["POST"])
def metaverse_transfer_api():
    data = request.json or {}
    try: return jsonify(transfer_myz(data.get("from_id"), data.get("to_id"), data.get("amount")))
    except (ValueError, TypeError) as exc: return jsonify({"error": str(exc)}), 400

@app.route("/api/metaverse/economy/ledger", methods=["GET"])
def metaverse_ledger_api(): return jsonify(ledger)

@app.route("/api/metaverse/missions", methods=["GET", "POST"])
def metaverse_missions_api():
    if request.method == "GET": return jsonify(list(metaverse_missions.values()))
    return jsonify(create_metaverse_mission(request.json or {})), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
