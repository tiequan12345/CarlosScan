from web3 import Web3
import token_fetcher
import pools_fetcher
import time

def fetch_all(chain, project, user, strategy):
  for attempt in range(5):
    try:
      return try_fetch_all(chain, project, user, strategy)
    except Exception as e:
      if "DECRYPTION_FAILED_OR_BAD_RECORD_MAC" not in str(e):
        print(f"Attempt {attempt+1}/5 failed with error: {e}")
      time.sleep(1)  # Wait before retrying
  
  print("Failed to fetch project details after multiple retries.")
  return None

def try_fetch_all(chain, project, user, strategy):
  web3 = Web3(Web3.HTTPProvider(chain['rpc']))
  
  # Override user with strategy in case strategy is set (allows for balance of strategy to show)
  if strategy and strategy in project.get('violin_strategy', {}):
    user = project['violin_strategy'][strategy]

  # Checksum config addresses as this is required by web3.py
  if isinstance(project["mc_address"], str):
    try:
      # For web3.py version 6+
      project['mc_address'] = Web3.to_checksum_address(project['mc_address'])
    except AttributeError:
      # For older web3.py versions
      project['mc_address'] = Web3.toChecksumAddress(project['mc_address'])
      
  try:
    # For web3.py version 6+
    project['native_token_address'] = Web3.to_checksum_address(project['native_token_address'])
  except AttributeError:
    # For older web3.py versions
    project['native_token_address'] = Web3.toChecksumAddress(project['native_token_address'])

  # Calculate the native token details
  pricer = web3.eth.contract(address=chain['pricer'], abi='[{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IPricer","name":"oldImplementation","type":"address"},{"indexed":true,"internalType":"contract IPricer","name":"newImplementation","type":"address"}],"name":"ImplementationChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousPendingOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newPendingOwner","type":"address"}],"name":"PendingOwnershipTransferred","type":"event"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"bytes","name":"metadata","type":"bytes"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"bytes[]","name":"metadata","type":"bytes[]"}],"name":"getPrices","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"metadata","type":"bytes"}],"name":"getValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes[]","name":"metadata","type":"bytes[]"}],"name":"getValues","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"contract IPricer","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IPricer","name":"_implementation","type":"address"}],"name":"setImplementation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPendingOwner","type":"address"}],"name":"setPendingOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

  # Get native token price either from config or from the price oracle
  if "native_price" in project:
    project['native_price'] = project["native_price"]
  else:
    project['native_price'] = pricer.functions.getPrice(project['native_token_address'], "0x").call()/1e18
  
  # Get native token details
  native_token = token_fetcher.to_contract(web3, project['native_token_address'])
  project['native_name'] = native_token.functions.name().call()
  project['native_symbol'] = native_token.functions.symbol().call()
  project['native_decimals'] = native_token.functions.decimals().call()
  project['project_name'] = project['native_name'].lower().replace("token", "").strip()

  # Fetch all pools and calculate reward information
  (project['pools'], project['dollar_rewards_per_second'], project['reward_rate']) = pools_fetcher.fetch_all(chain, project, user)

  # Calculate totals
  project['total_alloc_points'] = 0
  project['total_deposit_value'] = 0
  project['total_value_locked'] = 0
  project['total_pending'] = 0
  
  for pool in project['pools']:
    project['total_value_locked'] += pool['tvl']
    project['total_deposit_value'] += pool['user_value']
    project['total_alloc_points'] += pool['alloc_points']
    project['total_pending'] += pool.get("pending_rewards", 0)
    
  # Use total alloc points from contract if specified
  if project.get('use_total_alloc_points', False):
    try:
      mc = web3.eth.contract(address=project['mc_address'], abi=project['mc_abi'])
      project['total_alloc_points'] = mc.functions.totalAllocPoint().call()
    except Exception as e:
      print(f"Warning: Failed to fetch totalAllocPoint from contract: {e}")
      
  return project