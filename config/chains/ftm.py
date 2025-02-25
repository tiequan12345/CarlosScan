config = {
        "name": "ftm",
        "pricer": "0x393c80eD875eDe4dc9da8E5C9CA8959c5A36d6b4",
        #"rpc": "https://go.getblock.io/2f6a26f8d18b4b44a4003dc33b421293",
        #"rpc": "https://1rpc.io/ftm",
        #"rpc": "https://rpc2.fantom.network",
        #"rpc": "https://lb.drpc.org/ogrpc?network=fantom&dkey=Ao2Dk4jpt0u9uQK3thBPAftOuNGbsVUR75rlDonbV6cR",
        #"rpc": "https://fantom-mainnet.g.alchemy.com/v2/g5AnA4irWguo9iDa3I2-kdrGbff_w44d",
        "rpc": "https://site1.moralis-nodes.com/fantom/016e3b8c5cc64f25b92164c3ba7bbc69",
        "api": "https://api.ftmscan.com/api",
        "apikey": "9RPHTN9W4E3IVAR7K528JJE6W74S7FQKYI",
        "explorer": "https://ftmscan.com",
        "block_interval": 1
    }
    
def get_config():
    return config
    
def get_name():
    return config['name']