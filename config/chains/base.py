import os

config = { 
    "name": "base",
    "pricer": "0x43bEa134Ce66fC4cf90d3afA4c2eBCD0aC2a1D43",
    "api": "https://rpc.ankr.com/base",
    "explorer": "https://basescan.org",
    "block_interval": 2
}

# Fetch RPC from environment variable or provide a default
config["rpc"] = os.environ.get("BASE_RPC_URL", "DEFAULT_BASE_RPC_URL")

def get_config():
    return config
    
def get_name():
    return config['name']