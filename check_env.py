import os
from dotenv import load_dotenv

# Load from root .env
load_dotenv(".env")
print(f"Root .env DATABASE_URL: {os.getenv('DATABASE_URL')}")

# Load from backend/.env
load_dotenv("backend/.env", override=True)
print(f"Backend .env DATABASE_URL: {os.getenv('DATABASE_URL')}")
