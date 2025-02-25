config = {
        "name": "bsc",
        "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
        "rpc": "https://rpc.ankr.com/bsc",
        #"rpc": "https://speedy-nodes-nyc.moralis.io/103e0e4961730c735f3ceb65/bsc/mainnet/archive",
        "api": "https://api.bscscan.com/api",
        "apikey": "ZT5KEHKJIZJTZFPTXQ1E17EYVM8HN6QJMW",
        "explorer": "https://bscscan.com",
        "block_interval": 3
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']