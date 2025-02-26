import os

config = {
        "name": "ftm",
        "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
        "api": "https://api.ftmscan.com/api",
        "explorer": "https://ftmscan.com",
        "block_interval": 1
    }

# Fetch RPC from environment variable or provide a default
config["rpc"] = os.environ.get("FTM_RPC_URL", "DEFAULT_FTM_RPC_URL")
    
def get_config():
    return config
    
def get_name():
    return config['name']