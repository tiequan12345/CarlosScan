config = {
        "name": "metis",
        "pricer": "0x4bAeFD514e0f7d51C510c5139a1a736a56296964",
        "rpc": "https://andromeda.metis.io/?owner=1088",
        #"rpc": "https://rpc.cronaswap.org/",
        # "rpc": "https://cronosrpc-1.xstaking.sg/",
        "block_interval": 2.8,
        "explorer": "https://andromeda-explorer.metis.io",
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']