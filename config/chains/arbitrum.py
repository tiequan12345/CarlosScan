import os

config = {
    "name": "arbitrum",
    "pricer": "0x7495Bd05276CD4B192e315fAf891759039fA5884",
    "api": "https://api.arbiscan.io/api",
    "explorer": "https://snowtrace.io",
    "block_interval": 12
}

# Fetch RPC from environment variable or provide a default
config["rpc"] = os.environ.get("ARBITRUM_RPC_URL", "DEFAULT_ARBITRUM_RPC_URL")

def get_config():
    return config
    
def get_name():
    return config['name']