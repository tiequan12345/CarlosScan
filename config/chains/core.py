config = {
        "name": "core",
        "pricer": "0x7495Bd05276CD4B192e315fAf891759039fA5884",
        "rpc": "https://rpc-core.icecreamswap.com",
        "block_interval": 3,
        "api": "https://api.cronoscan.com/api",
        "explorer": "https://scan.coredao.org/",
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']