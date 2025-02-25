config = {
    "name": "moonbeam",
    "pricer": "0xe7aBd3963B497Bb97Cba431Bc156002Fb339262F",
    #"rpc": "https://rpc.api.moonbeam.network",
    "rpc": "https://moonbeam.public.blastapi.io",
    "block_interval": 12.35
}

def get_config():
    return config
    
def get_name():
    return config['name']