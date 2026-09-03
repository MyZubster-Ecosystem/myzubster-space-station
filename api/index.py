import importlib.util
from pathlib import Path

app_path = Path(__file__).resolve().parents[1] / "station-core" / "app.py"
spec = importlib.util.spec_from_file_location("station_core_app", app_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = module.app
