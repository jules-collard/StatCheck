import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = f"http://{os.getenv("BACKEND_URL")}/api"