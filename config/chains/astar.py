config = {
    "name": "astar",
    "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
    "rpc": "https://rpc.astar.network:8545",        
    #"rpc": "https://speedy-nodes-nyc.moralis.io/6292a1e8f63ffbace72c0a8b/avalanche/mainnet",
    "explorer": "https://blockscout.com/astar",
    "block_interval": 14.4
}

def get_config():
    return config

def get_name():
    return config["name"]