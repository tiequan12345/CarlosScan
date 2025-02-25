config = {
    "name": "thena",
    "chain": "bsc",
    "mc_address": [
        "0x7144851e51523a88EA6BeC9710cC07f3a9B3baa7", #BNB/BUSD
        "0x41adA56DD5702906549a71666541a39B0DbcEb12", # BUSD/USDT
        "0x9A0C07d7b9d0e0A82ccb12049876e2FB6bf96D0f", #ETH/BNB
        "0xDD35503b77277a6D810fEa6479C92bbCE5bbb412", # BTCB/BNB
        "0x0Df5Dfe92A0568373DA2d705Cdb5F68017c4B19A", # BNB/BNBx
        "0x11e79bc17cb1ff3d4f6a025412ac84960b20ba81", # BUSD/USDC
        "0xf26c84237f6c4a2268ac1d699475d2e07689ffb4", # stkBNB/BNB
        "0x19549316a62f1d333ca7656ba634ba3cab843348", # FRAX/BUSD
        "0x896256c48341B8E2B16AcFc9189D844624bD609B", # BNB/AVAX
        "0x96bead3ab5e281add000e468ab862a59f55223a7", # BUSD/USDC
        "0x19Beb32Dc0fB085Ef372E96E946BE21eCeE3fC51", # USDT/USDC
        "0x638b0cc37ffe5a040079F75Ae6C50C9A386dDCaF" #BNB/THE
    ],
    "native_token_address": "0xF4C8E32EaDEC4BFe97E0F595AdD0f4450a863a11",
    "reward_rate_function": "rewardRate()",
    "staking_token_function": "TOKEN()",
    "balance_function": "balanceOf(address)",
    "rewards_per_second": True,
    #"throttle": 5,
    "violin_strategy": {
        "carlos": "0x66FAb10EB7562D43070e71D9A28Ec57db1920D6D",
        "mk": "0x86a21C727C6d1e96FB9eC68e3fB13ee228DBaf06",

    },
    "mc_abi": '[{"inputs":[{"internalType":"address","name":"_rewardToken","type":"address"},{"internalType":"address","name":"_ve","type":"address"},{"internalType":"address","name":"_token","type":"address"},{"internalType":"address","name":"_distribution","type":"address"},{"internalType":"address","name":"_internal_bribe","type":"address"},{"internalType":"address","name":"_external_bribe","type":"address"},{"internalType":"bool","name":"_isForPair","type":"bool"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"claimed0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"claimed1","type":"uint256"}],"name":"ClaimFees","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"Harvest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"RewardAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"DISTRIBUTION","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DURATION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TOKEN","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_VE","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"_balances","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_periodFinish","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimFees","outputs":[{"internalType":"uint256","name":"claimed0","type":"uint256"},{"internalType":"uint256","name":"claimed1","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"depositAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"earned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"external_bribe","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"fees0","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"fees1","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"gaugeRewarder","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"internal_bribe","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isForPair","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastTimeRewardApplicable","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastUpdateTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"reward","type":"uint256"}],"name":"notifyRewardAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"periodFinish","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardForDuration","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardPerToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardPerTokenStored","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewarderPid","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"rewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_distribution","type":"address"}],"name":"setDistribution","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_gaugeRewarder","type":"address"}],"name":"setGaugeRewarder","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"setRewarderPid","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userRewardPerTokenPaid","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdrawAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdrawAllAndHarvest","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
}

def get_config():
    return config
    
def get_name():
    return config['name']