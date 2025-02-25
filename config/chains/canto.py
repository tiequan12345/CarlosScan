config = {
        "name": "canto",
        "pricer": "0x7495Bd05276CD4B192e315fAf891759039fA5884",
        "rpc": "https://canto.slingshot.finance",
        "block_interval": 6,
        "api": "https://api.cronoscan.com/api",
        "explorer": "https://cronoscan.com",
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']