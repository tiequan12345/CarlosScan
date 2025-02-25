config = {
    "name": "kava",
    "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
    #"rpc": "https://evm.kava.io",
    "rpc": "https://evm2.kava.io",
    "explorer": "https://explorer.kava.io/",
    "block_interval": 6.7
}

def get_config():
    return config

def get_name():
    return config["name"]