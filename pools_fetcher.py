from web3 import Web3
from importlib import reload

import token_fetcher
import pool_fetcher

from multiprocessing import Process, Pool
from contextlib import closing

def fetch_pool(data):
  chain = data['chain']
  project = data['project']
  user = data['user']
  pid = data['pid']
  lp_summary = project.get('lp_summary', False)
  
  try:
    web3 = Web3(Web3.HTTPProvider(chain['rpc']))
    
    # Check if pricer is in chain config, otherwise use default
    if 'pricer' in chain:
        pricer_addr = chain['pricer']
    else:
        print(f"Warning: No pricer address in chain config, using project pricer or default")
        pricer_addr = project.get('pricer', '0x7FA4b073CCf898c97299ac5aCEb5dE8d5Ef2c7f6')
    
    try:
        pricer_addr = Web3.to_checksum_address(pricer_addr)
    except AttributeError:
        # For older web3.py versions
        pricer_addr = Web3.toChecksumAddress(pricer_addr)
        
    pricer = web3.eth.contract(address=pricer_addr, abi='[{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IPricer","name":"oldImplementation","type":"address"},{"indexed":true,"internalType":"contract IPricer","name":"newImplementation","type":"address"}],"name":"ImplementationChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousPendingOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newPendingOwner","type":"address"}],"name":"PendingOwnershipTransferred","type":"event"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"bytes","name":"metadata","type":"bytes"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"bytes[]","name":"metadata","type":"bytes[]"}],"name":"getPrices","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"metadata","type":"bytes"}],"name":"getValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes[]","name":"metadata","type":"bytes[]"}],"name":"getValues","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"contract IPricer","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IPricer","name":"_implementation","type":"address"}],"name":"setImplementation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPendingOwner","type":"address"}],"name":"setPendingOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

    mc = web3.eth.contract(address=project['mc_address'], abi=project['mc_abi'])

    pool_info = mc.functions.poolInfo(pid).call()

    user_pending_rewards = 0
    
    if "pending_rewards_function" in project and project['pending_rewards_function']:
      try:
        user_pending_rewards = mc.get_function_by_signature(project['pending_rewards_function'])(pid, user).call()
      except Exception as e:
        print(f"Error fetching pending rewards for pid {pid}: {e}")
        
    token_address = mc.get_function_by_signature(project['token_address_function'])(pid).call() if "token_address_function" in project else pool_info[0]
    token = token_fetcher.to_contract(web3, token_address)
    supplied = pool_info[project["lpSupply"]] if "lpSupply" in project else token.functions.balanceOf(project['mc_address']).call()
    user_stake = mc.functions.userInfo(pid, user).call()[0]
    alloc_points = pool_info[project["allocPoints"]] if "allocPoints" in project else pool_info[1]
    
    return pool_fetcher.get_pool(web3, pricer, project, {
      "pid": pid,
      "token_address": token_address,
      "token": token,
      "user_stake": user_stake,
      "alloc_points": alloc_points,
      "supplied": supplied,
      "pending_rewards": user_pending_rewards
    }, lp_summary)
  except Exception as e:
    print(f"Error fetching pool {pid}: {e}")
    return None

def fetch_all(chain, project, user):
  web3 = Web3(Web3.HTTPProvider(chain['rpc']))

  pools = []
  dollar_rewards_per_second = 0
  reward_rate = 0
  user_pending_rewards = False
  reward_rate_function_args = project.get("reward_rate_function_args", [])

  # Get pricer address
  if 'pricer' in chain:
    pricer_addr = chain['pricer']
  else:
    print(f"Warning: No pricer address in chain config, using project pricer or default")
    pricer_addr = project.get('pricer', '0x7FA4b073CCf898c97299ac5aCEb5dE8d5Ef2c7f6')
  
  try:
    pricer_addr = Web3.to_checksum_address(pricer_addr)
  except AttributeError:
    # For older web3.py versions
    pricer_addr = Web3.toChecksumAddress(pricer_addr)
    
  pricer_abi = '[{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IPricer","name":"oldImplementation","type":"address"},{"indexed":true,"internalType":"contract IPricer","name":"newImplementation","type":"address"}],"name":"ImplementationChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousPendingOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newPendingOwner","type":"address"}],"name":"PendingOwnershipTransferred","type":"event"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"bytes","name":"metadata","type":"bytes"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"bytes[]","name":"metadata","type":"bytes[]"}],"name":"getPrices","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"metadata","type":"bytes"}],"name":"getValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes[]","name":"metadata","type":"bytes[]"}],"name":"getValues","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"contract IPricer","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IPricer","name":"_implementation","type":"address"}],"name":"setImplementation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPendingOwner","type":"address"}],"name":"setPendingOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

  # Synthetix like contracts are supported here
  if isinstance(project['mc_address'], list):
    pricer = web3.eth.contract(address=pricer_addr, abi=pricer_abi)
    for mc_address in project['mc_address']:
      try:
        try:
          # For web3.py version 6+
          mc_address = Web3.to_checksum_address(mc_address)
        except AttributeError:
          # For older web3.py versions
          mc_address = Web3.toChecksumAddress(mc_address)
        mc = web3.eth.contract(address=mc_address, abi=project['mc_abi'])
        token_address = mc.get_function_by_signature(project['staking_token_function'])().call()
        token = token_fetcher.to_contract(web3, token_address)
        supplied = token.functions.balanceOf(mc_address).call()
        user_stake = mc.get_function_by_signature(project['balance_function'])(user).call()
        
        user_pending_rewards = 0
        if "pending_rewards_function" in project and project['pending_rewards_function']:
          try:
            user_pending_rewards = mc.get_function_by_signature(project['pending_rewards_function'])(user).call()
          except Exception as e:
            print(f"Error fetching pending rewards: {e}")
            
        multiplier = project.get('multiplier', 1)
        alloc_points = (multiplier * mc.get_function_by_signature(project['reward_rate_function'])(*reward_rate_function_args).call())/(10**project['native_decimals'])
        
        reward_rate_pool = alloc_points if project['rewards_per_second'] else alloc_points / chain['block_interval']
        reward_rate += reward_rate_pool
        dollar_rewards_per_second += reward_rate_pool * project['native_price']
        
        pool_result = pool_fetcher.get_pool(web3, pricer, project, {
          "pid": mc_address,
          "token_address": token_address,
          "token": token,
          "user_stake": user_stake,
          "alloc_points": alloc_points,
          "supplied": supplied,
          "pending_rewards": user_pending_rewards
        }, project.get('lp_summary', False))
        
        if pool_result:
          pools.append(pool_result)
      except Exception as e:
        print(f"Error processing masterchef at {mc_address}: {e}")
  # Masterchef like contracts are supported here
  else:
    try:
      # Ensure the MC address is checksummed
      if isinstance(project['mc_address'], str):
        try:
          if not web3.is_checksum_address(project['mc_address']):
            project['mc_address'] = web3.to_checksum_address(project['mc_address'])
        except AttributeError:
          # For older web3.py versions
          if not web3.isChecksumAddress(project['mc_address']):
            project['mc_address'] = web3.toChecksumAddress(project['mc_address'])
      
      mc = web3.eth.contract(address=project['mc_address'], abi=project['mc_abi'])
      multiplier = project.get('multiplier', 1)
      
      # Ensure native token address is checksummed
      try:
        if not web3.is_checksum_address(project['native_token_address']):
          project['native_token_address'] = web3.to_checksum_address(project['native_token_address'])
      except AttributeError:
        # For older web3.py versions
        if not web3.isChecksumAddress(project['native_token_address']):
          project['native_token_address'] = web3.toChecksumAddress(project['native_token_address'])
          
      native_token = token_fetcher.to_contract(web3, project['native_token_address'])
      native_decimals = native_token.functions.decimals().call()
      
      reward_rate_raw = (multiplier * mc.get_function_by_signature(project['reward_rate_function'])(*reward_rate_function_args).call())/(10**native_decimals)
      reward_rate = reward_rate_raw if project['rewards_per_second'] else reward_rate_raw / chain['block_interval']
      dollar_rewards_per_second = reward_rate * project.get('native_price', 1.0)

      pool_length = project.get('poolLength', mc.functions.poolLength().call())

      requests = []
      for pid in range(pool_length):
        requests.append({"chain": chain, "project": project, "user": user, "pid": pid})
        
      # Process in parallel if enabled, otherwise sequentially
      valid_pools = []
      if project.get('parallel', False):
        with closing(Pool(processes=min(pool_length, 8))) as thread_pool:
          pool_results = thread_pool.map(fetch_pool, requests)
          valid_pools = [p for p in pool_results if p is not None]
      else:
        for req in requests:
          pool_result = fetch_pool(req)
          if pool_result:
            valid_pools.append(pool_result)
      
      # Only include pools with non-zero allocations if hide_no_rewards is enabled
      if project.get('hide_no_rewards', False):
        pools = [p for p in valid_pools if p['alloc_points'] > 0]
      else:
        pools = valid_pools
        
    except Exception as e:
      print(f"Error fetching masterchef data: {e}")

  return pools, dollar_rewards_per_second, reward_rate