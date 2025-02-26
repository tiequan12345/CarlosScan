import os

config = {
    "name": "eth",
    "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
    "block_interval": 13,
}

# Fetch RPC from environment variable or provide a default
config["rpc"] = os.environ.get("ETH_RPC_URL", "DEFAULT_ETH_RPC_URL")
    
def get_config():
    return config
    
def get_name():
    return config['name']