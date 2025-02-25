config = {
    "name": "arbitrum",
    "pricer": "0x7495Bd05276CD4B192e315fAf891759039fA5884",
    "api": "https://api.arbiscan.io/api",
    "rpc": "https://arbitrum-one.gateway.pokt.network/v1/lb/1dcba20debbba0da7e4a2068",
    "apikey": "DBQ3BPTFG7ATR31CK9N9ZXS6IBDCETVPUN",
    #"rpc": "https://arbitrum-one.gateway.pokt.network/v1/lb/1dcba20debbba0da7e4a2068",
    "block_interval": 12
}

def get_config():
    return config
    
def get_name():
    return config['name']