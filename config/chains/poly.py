import os

config = {
        "name": "poly",
        "pricer": "0x75fB02aFAB420fBeed53B5Ee3703b91fAb111fbD",
        "api": "https://api.polygonscan.com/api",
        "explorer": "https://polygonscan.com",
        "block_interval": 2.2
    }

# Fetch RPC from environment variable or provide a default
config["rpc"] = os.environ.get("POLY_RPC_URL", "DEFAULT_POLY_RPC_URL")
    
def get_config():
    return config
    
def get_name():
    return config['name']