config = {
    "name": "sonic",
    "chain_id": "sonic",  # Adding chain_id for price fetching
    "pricer": "0x7FA4b073CCf898c97299ac5aCEb5dE8d5Ef2c7f6",
    "rpc": "https://rpc.soniclabs.com",        
    #"rpc": "https://speedy-nodes-nyc.moralis.io/6292a1e8f63ffbace72c0a8b/avalanche/mainnet",
    "explorer": "https://sonicscan.org/",
    "block_interval": 0.3
}

def get_config():
    return config

def get_name():
    return config["name"]