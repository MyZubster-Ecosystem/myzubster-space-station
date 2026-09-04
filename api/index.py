import importlib.util
import sys
from pathlib import Path

station_core = Path(__file__).resolve().parents[1] / "station-core"
sys.path.insert(0, str(station_core))
app_path = station_core / "app.py"
spec = importlib.util.spec_from_file_location("station_core_app", app_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

flask_app = module.app

class PreserveApiPath:
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        original = environ.get("HTTP_X_VERCEL_ORIGINAL_PATH") or environ.get("HTTP_X_NOW_ROUTE_MATCHES")
        if original and original.startswith("/api/"):
            environ["PATH_INFO"] = original
        elif path in ("/api/index.py", "/index.py"):
            uri = environ.get("REQUEST_URI", "")
            if uri.startswith("/api/") and not uri.startswith("/api/index.py"):
                environ["PATH_INFO"] = uri.split("?", 1)[0]
        return self.app(environ, start_response)

app = PreserveApiPath(flask_app)
