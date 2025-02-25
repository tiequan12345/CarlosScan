config = {
        "name": "pulse",
        "pricer": "0xfaDcc2AFb4f9977575718E76DFfDb5e3838f5cB6",
        "rpc": "https://rpc.pulsechain.com",
        "block_interval": 10
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']