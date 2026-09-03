import importlib.util
import sys
from pathlib import Path

station_core = Path(__file__).resolve().parents[1] / "station-core"
sys.path.insert(0, str(station_core))
app_path = station_core / "app.py"
spec = importlib.util.spec_from_file_location("station_core_app", app_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = module.app
