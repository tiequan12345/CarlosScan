from web3 import Web3
import token_fetcher
import pools_fetcher

def fetch_all(chain, project, wallet, strategy=""):
  # Use strategy if provided
  if strategy and 'violin_strategy' in project and strategy in project['violin_strategy']:
    wallet = project['violin_strategy'][strategy]
  
  web3 = Web3(Web3.HTTPProvider(chain['rpc']))
  
  # Ensure addresses are properly checksummed
  try:
    if not Web3.is_checksum_address(project['native_token_address']):
      project['native_token_address'] = Web3.to_checksum_address(project['native_token_address'])
    
    if isinstance(project['mc_address'], str):
      if not Web3.is_checksum_address(project['mc_address']):
        project['mc_address'] = Web3.to_checksum_address(project['mc_address'])
    elif isinstance(project['mc_address'], list):
      project['mc_address'] = [Web3.to_checksum_address(addr) if not Web3.is_checksum_address(addr) else addr for addr in project['mc_address']]
    
    if not Web3.is_checksum_address(wallet):
      wallet = Web3.to_checksum_address(wallet)
  except Exception as e:
    print(f"Error while checksumming addresses: {e}")
  
  # Get native token information
  try:
    native_token = token_fetcher.to_contract(web3, project['native_token_address'])
    native_decimals = native_token.functions.decimals().call()
    
    # Use explicit values from config if available, otherwise get from contract
    native_name = project.get('native_name')
    if not native_name:
      native_name = native_token.functions.name().call()
      
    native_symbol = project.get('native_symbol')
    if not native_symbol:
      native_symbol = native_token.functions.symbol().call()
  except Exception as e:
    native_decimals = 18  # Default to 18 decimals
    native_name = "Unknown Token"
    native_symbol = "UNKNOWN"
    
  project['native_decimals'] = native_decimals
  native_price = project.get('native_price', 1.0)  # Default price
  
  # Set default values for dollar_rewards_per_second and reward_rate in case pools_fetcher fails
  dollar_rewards_per_second = 0
  reward_rate = 0
  pools = []
  
  try:
    # Get pools, rewards rate and other data
    pools, dollar_rewards_per_second, reward_rate = pools_fetcher.fetch_all(chain, project, wallet)
  except Exception as e:
    print(f"Error in pools_fetcher.fetch_all: {e}")
  
  # Calculate total value locked and user deposits
  total_value_locked = sum([pool.get("tvl", 0) for pool in pools])
  total_alloc_points = sum([pool.get("alloc_points", 0) for pool in pools])
  total_deposit_value = sum([pool.get("user_value", 0) for pool in pools])
  
  # Calculate total pending rewards
  total_pending = sum([pool.get("pending_rewards", 0) for pool in pools])
  
  # Create result object
  return {
    "project_name": project['name'],
    "native_name": native_name,
    "native_symbol": native_symbol,
    "native_price": native_price,
    "native_token_address": project['native_token_address'],
    "native_decimals": native_decimals,
    "mc_address": project['mc_address'],
    "reward_rate": reward_rate,
    "dollar_rewards_per_second": dollar_rewards_per_second,
    "pools": pools,
    "total_value_locked": total_value_locked,
    "total_alloc_points": total_alloc_points,
    "total_deposit_value": total_deposit_value,
    "total_pending": total_pending
  }