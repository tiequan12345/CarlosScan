config = {
        "name": "poly",
        "pricer": "0x75fB02aFAB420fBeed53B5Ee3703b91fAb111fbD",
        #"rpc": "https://speedy-nodes-nyc.moralis.io/103e0e4961730c735f3ceb65/polygon/mainnet/archive",
        "rpc": "https://polygon-rpc.com",
        "api": "https://api.polygonscan.com/api",
        "apikey": "K5UTRNPZ2MM9M7XBFC2BR3SCDEHSP29VXH",
        "explorer": "https://polygonscan.com",
        "block_interval": 2.2
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']