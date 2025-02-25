config = {
    "name": "milkomeda",
    "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
    "rpc": "https://rpc-mainnet-cardano-evm.c1.milkomeda.com",
    "block_interval": 4
}

def get_config():
    return config
    
def get_name():
    return config['name']