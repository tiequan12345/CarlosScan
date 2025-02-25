config = {
    "name": "zksync",
    #"pricer": "0x7495Bd05276CD4B192e315fAf891759039fA5884",
    "api": "https://api.arbiscan.io/api",
    "rpc": "https://mainnet.era.zksync.io",
    #"rpc": "https://arbitrum-one.gateway.pokt.network/v1/lb/1dcba20debbba0da7e4a2068",
    "block_interval": 15,
    "explorer": "https://zksync2-mainnet.zkscan.io/"
}

def get_config():
    return config
    
def get_name():
    return config['name']