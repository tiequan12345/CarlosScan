import os

config = {
        "name": "cronos",
        "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
        "block_interval": 5.7,
        "api": "https://api.cronoscan.com/api",
        "explorer": "https://cronoscan.com",
    }

# Fetch RPC from environment variable or provide a default
config["rpc"] = os.environ.get("CRONOS_RPC_URL", "DEFAULT_CRONOS_RPC_URL")
    
def get_config():
    return config
    
def get_name():
    return config['name']