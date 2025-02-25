config = {
    "name": "eth",
    "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
    "rpc": "https://rpc.ankr.com/eth",
    "block_interval": 13,
    #"api": "https://api.etherscan.io/api",
    #"apikey": "4IHUST2E2QXEFAAJZIQMDVD45YBI3JDC22",
    #"explorer": "https://etherscan.io/"
}

def get_config():
    return config
    
def get_name():
    return config['name']