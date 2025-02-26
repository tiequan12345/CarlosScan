import os

config = {
        "name": "bsc",
        "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
        "api": "https://api.bscscan.com/api",
        "explorer": "https://bscscan.com",
        "block_interval": 3
    }

# Fetch RPC from environment variable or provide a default
config["rpc"] = os.environ.get("BSC_RPC_URL", "DEFAULT_BSC_RPC_URL")
    
def get_config():
    return config
    
def get_name():
    return config['name']