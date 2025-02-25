config = {
    "name": "avax",
    "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
    "rpc": "https://api.avax.network/ext/bc/C/rpc", 
    #"rpc": "https://rpc.ankr.com/avalanche",       
    #"rpc": "https://speedy-nodes-nyc.moralis.io/6292a1e8f63ffbace72c0a8b/avalanche/mainnet",
    "api": "https://api.snowtrace.io/api",
    "explorer": "https://snowtrace.io",
    "block_interval": 2
}

def get_config():
    return config

def get_name():
    return config["name"]