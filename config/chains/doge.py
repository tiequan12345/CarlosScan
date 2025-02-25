config = {
        "name": "doge",
        "pricer": "0x7495Bd05276CD4B192e315fAf891759039fA5884",
        "rpc": "https://rpc.dogechain.dog",
        #"rpc": "https://speedy-nodes-nyc.moralis.io/103e0e4961730c735f3ceb65/bsc/mainnet/archive",
        #"api": "https://api.bscscan.com/api",
        #"apikey": "ZT5KEHKJIZJTZFPTXQ1E17EYVM8HN6QJMW",
        "explorer": "https://explorer.dogechain.dog",
        "block_interval": 2
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']