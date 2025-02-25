config = {
    "name": "aurora",
    "pricer": "0xEAe270409435AdB1F400cc593356730971ecc37D",
    "rpc": "https://mainnet.aurora.dev",
    "block_interval": 1.3
}

def get_config():
    return config
    
def get_name():
    return config['name']