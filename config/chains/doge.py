import os

config = {
        "name": "doge",
        "pricer": "0x7495Bd05276CD4B192e315fAf891759039fA5884",
        "explorer": "https://explorer.dogechain.dog",
        "block_interval": 2
    }

# Fetch RPC from environment variable or provide a default
config["rpc"] = os.environ.get("DOGE_RPC_URL", "DEFAULT_DOGE_RPC_URL")
    
def get_config():
    return config
    
def get_name():
    return config['name']