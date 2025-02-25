config = {
        "name": "optimism",
        "pricer": "0x7495Bd05276CD4B192e315fAf891759039fA5884",
        "rpc": "https://rpc.ankr.com/optimism",
        "api": "",
        "apikey": "",
        "explorer": "https://optimistic.etherscan.io",
        "block_interval": 10
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']