config = {
        "name": "heco",
        "pricer": "0x7495Bd05276CD4B192e315fAf891759039fA5884",
        "rpc": "https://http-mainnet.hecochain.com/",
        #"rpc": "https://speedy-nodes-nyc.moralis.io/103e0e4961730c735f3ceb65/bsc/mainnet/archive",
        "explorer": "https://hecoinfo.com",
        "block_interval": 2.1
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']