# Loads in limited data about a pool and adds common details like price, lp breakup and so forth to it
import token_fetcher

def get_pool(web3, pricer, project, pool_data, lp_summary=False):
  try:
    price = pricer.functions.getPrice(pool_data["token_address"], "0x").call()
  except Exception as e:
    print(f"Error getting price for token {pool_data['token_address']}: {e}")
    # Default to 1.0 as price if fetching fails
    price = 1e18  # Set a default price of 1.0
  
  token = pool_data["token"]
  
  try:
    decimals = token.functions.decimals().call()
  except Exception as e:
    print(f"Error getting decimals for token {pool_data['token_address']}: {e}")
    decimals = 18  # Default to 18 decimals
    
  user_value = price * pool_data["user_stake"] /1e18/(10**decimals)
  pending_rewards = pool_data["pending_rewards"]
  
  pool = {
      "pid": pool_data["pid"],
      "token_address": pool_data["token_address"],
      "token_name": token.functions.name().call(),
      "token_symbol": token.functions.symbol().call(),
      "user_stake": pool_data["user_stake"]/(10**decimals),
      "user_value": user_value,
      "alloc_points": pool_data["alloc_points"],
      "is_lp": False,
      "supplied": pool_data["supplied"],
      "decimals": decimals,
      "price": price,
      "tvl": price * pool_data["supplied"] / 1e18/(10**decimals),
      "pending_rewards": (pending_rewards / (10**project['native_decimals'])) * project['native_price'] if pending_rewards else 0
  }
  try:
    token0_address = token.get_function_by_signature("token0()")().call()
    token0 = token_fetcher.to_contract(web3, token0_address)
    token1_address = token.get_function_by_signature("token1()")().call()
    token1 = token_fetcher.to_contract(web3, token1_address)
    token0_symbol = token0.functions.symbol().call() 
    token1_symbol = token1.functions.symbol().call() 
    pool['token0_symbol'] = token0_symbol
    pool['token1_symbol'] = token1_symbol
    pool['token_name'] = token0_symbol + "/" + token1_symbol
    pool['token0_address'] = token0_address
    pool['token1_address'] = token1_address
    if lp_summary:
      total_supply = token.functions.totalSupply().call()
      pool['token0_amount'] = token0.functions.balanceOf(token.address).call() * pool_data["user_stake"] / total_supply / (10**token0.functions.decimals().call())
      pool['token1_amount'] = token1.functions.balanceOf(token.address).call() * pool_data["user_stake"] / total_supply / (10**token1.functions.decimals().call())
  except Exception as e:
    # Silently continue if token doesn't have LP methods
    pass
  return pool