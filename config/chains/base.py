config = { 
    "name": "base",
    "pricer": "0x43bEa134Ce66fC4cf90d3afA4c2eBCD0aC2a1D43",
    "api": "https://rpc.ankr.com/base",
    #"rpc": "https://developer-access-mainnet.base.org",
    #"rpc": "https://1rpc.io/base",
    "rpc": "https://base.rpc.subquery.network/public",
    "apikey": "DBQ3BPTFG7ATR31CK9N9ZXS6IBDCETVPUN",
    #"rpc": "https://arbitrum-one.gateway.pokt.network/v1/lb/1dcba20debbba0da7e4a2068",
    "block_interval": 2
}

def get_config():
    return config
    
def get_name():
    return config['name']