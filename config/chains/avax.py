import os

config = {
    "name": "avax",
    "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
    "api": "https://api.snowtrace.io/api",
    "explorer": "https://snowtrace.io",
    "block_interval": 2
}

# Fetch RPC from environment variable or provide a default
config["rpc"] = os.environ.get("AVAX_RPC_URL", "DEFAULT_AVAX_RPC_URL")

def get_config():
    return config

def get_name():
    return config["name"]