config = {
        "name": "cronos",
        "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
        #"rpc": "https://evm-cronos.crypto.org",
        #"rpc": "https://rpc.cronaswap.org/",
        #"rpc": "https://rpc.artemisone.org/cronos",
        "rpc": "https://mmf-rpc.xstaking.sg",
        #"rpc": "https://cronosrpc-1.xstaking.sg/",
        "block_interval": 5.7,
        "api": "https://api.cronoscan.com/api",
        "explorer": "https://cronoscan.com",
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']