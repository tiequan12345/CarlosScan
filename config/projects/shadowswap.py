config = {
  "name": "shadowswap",
  "chain": "core",
  "mc_address": "0xc7887AF5F95CDEe2B7bbFf47554104E8631751Df",
  "violin_strategy": {
    "USDT-BUSD": "0x8B350905BdBf4c05ef6953376403B95702C0723A",
    "carlos": "0xCa031a8840Ee850884d38180c6302FF9B3BDb8F9",
    "mk": "0x363D94e7A2F54D33763d87eA390FC7f9cE86da9f"
  },
  "native_token_address": "0xddBa66C1eBA873e26Ac0215Ca44892a07d83aDF5",
  "reward_rate_function": "shdwPerBlock(bool)",
  "token_address_function": "lpToken(uint256)",
  "rewards_per_second": False,
  "allocPoints": 2,
  "reward_rate_function_args": [True],
  "mc_abi": '[{"inputs":[{"name":"_SHDW","internalType":"contract IBEP20","type":"address"},{"name":"_burnAdmin","internalType":"address","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"indexed":true,"name":"pid","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"allocPoint","internalType":"uint256","type":"uint256"},{"indexed":true,"name":"lpToken","internalType":"contract IBEP20","type":"address"},{"indexed":false,"name":"isRegular","internalType":"bool","type":"bool"}],"name":"AddPool","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"user","internalType":"address","type":"address"},{"indexed":true,"name":"pid","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"amount","internalType":"uint256","type":"uint256"}],"name":"Deposit","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"user","internalType":"address","type":"address"},{"indexed":true,"name":"pid","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"amount","internalType":"uint256","type":"uint256"}],"name":"EmergencyWithdraw","anonymous":false,"type":"event"},{"inputs":[{"indexed":false,"name":"burnRate","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"regularFarmRate","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"specialFarmRate","internalType":"uint256","type":"uint256"}],"name":"EventUpdateShdwRate","anonymous":false,"type":"event"},{"inputs":[],"name":"Init","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"previousOwner","internalType":"address","type":"address"},{"indexed":true,"name":"newOwner","internalType":"address","type":"address"}],"name":"OwnershipTransferred","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"pid","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"allocPoint","internalType":"uint256","type":"uint256"}],"name":"SetPool","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"boostContract","internalType":"address","type":"address"}],"name":"UpdateBoostContract","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"user","internalType":"address","type":"address"},{"indexed":false,"name":"pid","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"oldMultiplier","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"newMultiplier","internalType":"uint256","type":"uint256"}],"name":"UpdateBoostMultiplier","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"oldAdmin","internalType":"address","type":"address"},{"indexed":true,"name":"newAdmin","internalType":"address","type":"address"}],"name":"UpdateBurnAdmin","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"pid","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"lastRewardBlock","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"lpSupply","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"accShdwPerShare","internalType":"uint256","type":"uint256"}],"name":"UpdatePool","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"user","internalType":"address","type":"address"},{"indexed":false,"name":"isValid","internalType":"bool","type":"bool"}],"name":"UpdateWhiteList","anonymous":false,"type":"event"},{"inputs":[{"indexed":true,"name":"user","internalType":"address","type":"address"},{"indexed":true,"name":"pid","internalType":"uint256","type":"uint256"},{"indexed":false,"name":"amount","internalType":"uint256","type":"uint256"}],"name":"Withdraw","anonymous":false,"type":"event"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"ACC_SHDW_PRECISION","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"BOOST_PRECISION","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"MASTERCHEF_SHDW_PER_BLOCK","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"MAX_BOOST_PRECISION","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"contract IBEP20","type":"address"}],"inputs":[],"name":"SHDW","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"SHDW_RATE_TOTAL_PRECISION","stateMutability":"view","type":"function"},{"outputs":[],"inputs":[{"name":"_allocPoint","internalType":"uint256","type":"uint256"},{"name":"_lpToken","internalType":"contract IBEP20","type":"address"},{"name":"_isRegular","internalType":"bool","type":"bool"},{"name":"_withUpdate","internalType":"bool","type":"bool"}],"name":"add","stateMutability":"nonpayable","type":"function"},{"outputs":[{"name":"","internalType":"address","type":"address"}],"inputs":[],"name":"boostContract","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"address","type":"address"}],"inputs":[],"name":"burnAdmin","stateMutability":"view","type":"function"},{"outputs":[],"inputs":[{"name":"_withUpdate","internalType":"bool","type":"bool"}],"name":"burnShdw","stateMutability":"nonpayable","type":"function"},{"outputs":[],"inputs":[{"name":"_pid","internalType":"uint256","type":"uint256"},{"name":"_amount","internalType":"uint256","type":"uint256"}],"name":"deposit","stateMutability":"nonpayable","type":"function"},{"outputs":[],"inputs":[{"name":"_pid","internalType":"uint256","type":"uint256"}],"name":"emergencyWithdraw","stateMutability":"nonpayable","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[{"name":"_user","internalType":"address","type":"address"},{"name":"_pid","internalType":"uint256","type":"uint256"}],"name":"getBoostMultiplier","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"lastBurnedBlock","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"contract IBEP20","type":"address"}],"inputs":[{"name":"","internalType":"uint256","type":"uint256"}],"name":"lpToken","stateMutability":"view","type":"function"},{"outputs":[],"inputs":[],"name":"massUpdatePools","stateMutability":"nonpayable","type":"function"},{"outputs":[{"name":"","internalType":"address","type":"address"}],"inputs":[],"name":"owner","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[{"name":"_pid","internalType":"uint256","type":"uint256"},{"name":"_user","internalType":"address","type":"address"}],"name":"pendingShdw","stateMutability":"view","type":"function"},{"outputs":[{"name":"accShdwPerShare","internalType":"uint256","type":"uint256"},{"name":"lastRewardBlock","internalType":"uint256","type":"uint256"},{"name":"allocPoint","internalType":"uint256","type":"uint256"},{"name":"totalBoostedShare","internalType":"uint256","type":"uint256"},{"name":"isRegular","internalType":"bool","type":"bool"}],"inputs":[{"name":"","internalType":"uint256","type":"uint256"}],"name":"poolInfo","stateMutability":"view","type":"function"},{"outputs":[{"name":"pools","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"poolLength","stateMutability":"view","type":"function"},{"outputs":[],"inputs":[],"name":"renounceOwnership","stateMutability":"nonpayable","type":"function"},{"outputs":[],"inputs":[{"name":"_pid","internalType":"uint256","type":"uint256"},{"name":"_allocPoint","internalType":"uint256","type":"uint256"},{"name":"_withUpdate","internalType":"bool","type":"bool"}],"name":"set","stateMutability":"nonpayable","type":"function"},{"outputs":[{"name":"amount","internalType":"uint256","type":"uint256"}],"inputs":[{"name":"_isRegular","internalType":"bool","type":"bool"}],"name":"shdwPerBlock","stateMutability":"view","type":"function"},{"outputs":[{"name":"amount","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"shdwPerBlockToBurn","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"shdwRateToBurn","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"shdwRateToRegularFarm","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"shdwRateToSpecialFarm","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"totalRegularAllocPoint","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"uint256","type":"uint256"}],"inputs":[],"name":"totalSpecialAllocPoint","stateMutability":"view","type":"function"},{"outputs":[],"inputs":[{"name":"newOwner","internalType":"address","type":"address"}],"name":"transferOwnership","stateMutability":"nonpayable","type":"function"},{"outputs":[],"inputs":[{"name":"_newBoostContract","internalType":"address","type":"address"}],"name":"updateBoostContract","stateMutability":"nonpayable","type":"function"},{"outputs":[],"inputs":[{"name":"_user","internalType":"address","type":"address"},{"name":"_pid","internalType":"uint256","type":"uint256"},{"name":"_newMultiplier","internalType":"uint256","type":"uint256"}],"name":"updateBoostMultiplier","stateMutability":"nonpayable","type":"function"},{"outputs":[],"inputs":[{"name":"_newAdmin","internalType":"address","type":"address"}],"name":"updateBurnAdmin","stateMutability":"nonpayable","type":"function"},{"outputs":[{"components":[{"name":"accShdwPerShare","internalType":"uint256","type":"uint256"},{"name":"lastRewardBlock","internalType":"uint256","type":"uint256"},{"name":"allocPoint","internalType":"uint256","type":"uint256"},{"name":"totalBoostedShare","internalType":"uint256","type":"uint256"},{"name":"isRegular","internalType":"bool","type":"bool"}],"name":"pool","internalType":"struct ShadowChefV2.PoolInfo","type":"tuple"}],"inputs":[{"name":"_pid","internalType":"uint256","type":"uint256"}],"name":"updatePool","stateMutability":"nonpayable","type":"function"},{"outputs":[],"inputs":[{"name":"_burnRate","internalType":"uint256","type":"uint256"},{"name":"_regularFarmRate","internalType":"uint256","type":"uint256"},{"name":"_specialFarmRate","internalType":"uint256","type":"uint256"},{"name":"_withUpdate","internalType":"bool","type":"bool"}],"name":"updateShdwRate","stateMutability":"nonpayable","type":"function"},{"outputs":[],"inputs":[{"name":"_user","internalType":"address","type":"address"},{"name":"_isValid","internalType":"bool","type":"bool"}],"name":"updateWhiteList","stateMutability":"nonpayable","type":"function"},{"outputs":[{"name":"amount","internalType":"uint256","type":"uint256"},{"name":"rewardDebt","internalType":"uint256","type":"uint256"},{"name":"boostMultiplier","internalType":"uint256","type":"uint256"}],"inputs":[{"name":"","internalType":"uint256","type":"uint256"},{"name":"","internalType":"address","type":"address"}],"name":"userInfo","stateMutability":"view","type":"function"},{"outputs":[{"name":"","internalType":"bool","type":"bool"}],"inputs":[{"name":"","internalType":"address","type":"address"}],"name":"whiteList","stateMutability":"view","type":"function"},{"outputs":[],"inputs":[{"name":"_pid","internalType":"uint256","type":"uint256"},{"name":"_amount","internalType":"uint256","type":"uint256"}],"name":"withdraw","stateMutability":"nonpayable","type":"function"}]'
   }

def get_config():
    return config
    
def get_name():
    return config['name']