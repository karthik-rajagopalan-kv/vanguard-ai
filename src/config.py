import os

QDRANT_API_URL = os.environ.get("QDRANT_API_URL", "http://localhost:6333")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", None)