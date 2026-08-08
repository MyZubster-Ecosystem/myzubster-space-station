#!/usr/bin/env python3
import requests
import time
import random
from datetime import datetime

class EvaIoniSimulator:
    def __init__(self, core_url="http://localhost:8001", robot_id="eva-ioni-001"):
        self.core_url = core_url
        self.robot_id = robot_id
        self.running = True
        self.position = {"x": 0, "y": 0, "z": 0}
        
    def generate_telemetry(self):
        return {
            "robot_id": self.robot_id,
            "temperature": round(random.uniform(18.0, 30.0), 1),
            "humidity": round(random.uniform(30.0, 70.0), 1),
            "battery": random.randint(70, 100),
            "location": self.position.copy()
        }
    
    def send_telemetry(self):
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
    
    def run(self):
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
    simulator = EvaIoniSimulator()
    try:
        simulator.run()
    except KeyboardInterrupt:
        print("\n🛑 Simulator stopped")
        simulator.stop()
