#!/usr/bin/env python3
"""
EVA IONI - Space Station Simulator
Simulates a robot sending telemetry data to the station core
"""

import requests
import time
import random
import json
from datetime import datetime

class EvaIoniSimulator:
    def __init__(self, core_url="http://localhost:8000", robot_id="eva-ioni-001"):
        self.core_url = core_url
        self.robot_id = robot_id
        self.running = True
        self.position = {"x": 0, "y": 0, "z": 0}
        
    def generate_telemetry(self):
        """Generate random telemetry data"""
        return {
            "robot_id": self.robot_id,
            "temperature": round(random.uniform(18.0, 30.0), 1),
            "humidity": round(random.uniform(30.0, 70.0), 1),
            "battery": random.randint(70, 100),
            "location": self.position.copy()
        }
    
    def send_telemetry(self):
        """Send telemetry to station core"""
        data = self.generate_telemetry()
        try:
            response = requests.post(
                f"{self.core_url}/api/telemetry",
                json=data,
                timeout=5
            )
            if response.status_code == 201:
                print(f"[{datetime.now().isoformat()}] ✅ Telemetry sent: {data}")
            else:
                print(f"[{datetime.now().isoformat()}] ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] ❌ Connection error: {e}")
    
    def move(self, direction, steps=1):
        """Move the robot in a direction"""
        if direction == "forward":
            self.position["x"] += steps
        elif direction == "backward":
            self.position["x"] -= steps
        elif direction == "left":
            self.position["y"] -= steps
        elif direction == "right":
            self.position["y"] += steps
        elif direction == "up":
            self.position["z"] += steps
        elif direction == "down":
            self.position["z"] -= steps
        else:
            print(f"Unknown direction: {direction}")
    
    def run(self):
        """Main loop"""
        print(f"🚀 EVA IONI Simulator starting...")
        print(f"📡 Core URL: {self.core_url}")
        print(f"🤖 Robot ID: {self.robot_id}")
        print("Press Ctrl+C to stop\n")
        
        while self.running:
            self.send_telemetry()
            time.sleep(5)
    
    def stop(self):
        self.running = False

if __name__ == "__main__":
    import sys
    
    simulator = EvaIoniSimulator()
    
    try:
        simulator.run()
    except KeyboardInterrupt:
        print("\n🛑 Simulator stopped")
        simulator.stop()
        sys.exit(0)
