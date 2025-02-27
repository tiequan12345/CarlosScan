from flask import Flask, render_template, request, jsonify
import config_fetcher
import project_fetcher
import json
import sys
import traceback
import requests
import time
from threading import Lock
import os

app = Flask(__name__)

# Cache for project and chain data
cache = {
    'projects': None,
    'chains': None,
    'token_prices': {},  # New cache for token prices
    'last_price_update': {}  # Track when prices were last updated
}

# Lock for thread safety when updating prices
price_lock = Lock()

# Time between price updates (3 minutes in seconds)
PRICE_UPDATE_INTERVAL = 180

def get_token_price(chain_id, token_address):
    """Get token price from DexScreener API with caching"""
    cache_key = f"{chain_id}_{token_address}"
    
    # Log the token address
    
    with price_lock:
        current_time = time.time()
        # Check if we have a cached price that's still fresh
        if (cache_key in cache['token_prices'] and 
            cache_key in cache['last_price_update'] and
            current_time - cache['last_price_update'][cache_key] < PRICE_UPDATE_INTERVAL):
            return cache['token_prices'][cache_key]
        
        # If not, fetch new price
        try:
            # Try multiple price sources
            price = None
            token_name = None
            token_symbol = None
            
            # 1. Try DexScreener API first
            try:
                # Try different API endpoints - first for pairs
                dexscreener_api_url = os.environ.get("DEXSCREENER_API_URL", "https://api.dexscreener.com/latest/dex/pairs")
                url = f"{dexscreener_api_url}/{chain_id}/{token_address}"
                response = requests.get(url, timeout=10)
                response_text = response.text
                
                if response.status_code == 200:
                    data = response.json()
                    if data and 'pairs' in data and data['pairs'] and len(data['pairs']) > 0:
                        price = float(data['pairs'][0]['priceUsd'])
                        # Get token info from the baseToken or quoteToken depending on which matches our address
                        if 'baseToken' in data['pairs'][0] and data['pairs'][0]['baseToken']['address'].lower() == token_address.lower():
                            token_name = data['pairs'][0]['baseToken'].get('name')
                            token_symbol = data['pairs'][0]['baseToken'].get('symbol')
                        elif 'quoteToken' in data['pairs'][0] and data['pairs'][0]['quoteToken']['address'].lower() == token_address.lower():
                            token_name = data['pairs'][0]['quoteToken'].get('name')
                            token_symbol = data['pairs'][0]['quoteToken'].get('symbol')
                    else:
                        # If pairs endpoint failed, try tokens endpoint
                        tokens_url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
                        tokens_response = requests.get(tokens_url, timeout=10)
                        
                        if tokens_response.status_code == 200:
                            tokens_data = tokens_response.json()
                            if tokens_data and 'pairs' in tokens_data and tokens_data['pairs'] and len(tokens_data['pairs']) > 0:
                                for pair in tokens_data['pairs']:
                                    if 'chainId' in pair and pair['chainId'] == chain_id:
                                        price = float(pair['priceUsd'])
                                        # Get token info from the baseToken or quoteToken
                                        if 'baseToken' in pair and pair['baseToken']['address'].lower() == token_address.lower():
                                            token_name = pair['baseToken'].get('name')
                                            token_symbol = pair['baseToken'].get('symbol')
                                            break
                                        elif 'quoteToken' in pair and pair['quoteToken']['address'].lower() == token_address.lower():
                                            token_name = pair['quoteToken'].get('name')
                                            token_symbol = pair['quoteToken'].get('symbol')
                                            break
                            else:
                                print(f"DexScreener tokens API returned no data: {tokens_response.text}") # Keep incase response is useful for debugging in future.
                        else:
                            print(f"DexScreener tokens API failed with status {tokens_response.status_code}")  # Keep incase response is useful for debugging in future.
                else:
                    print(f"DexScreener API failed with status {response.status_code}: {response_text}")  # Keep incase response is useful for debugging in future.
            except Exception as e:
                print(f"Error using DexScreener: {str(e)}") # Keep incase response is useful for debugging in future.
            
            # 2. Try DexTools API as backup if configured (add your API key in env)
            if price is None and os.environ.get("DEXTOOLS_API_KEY"):
                try:
                    headers = {"X-API-KEY": os.environ.get("DEXTOOLS_API_KEY")}
                    dextools_url = f"https://api.dextools.io/v1/token/{chain_id}/{token_address}"
                    response = requests.get(dextools_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data and 'data' in data and 'price' in data['data']:
                            price = float(data['data']['price'])
                            # Try to get token name and symbol from DexTools response
                            if 'name' in data['data']:
                                token_name = data['data']['name']
                            if 'symbol' in data['data']:
                                token_symbol = data['data']['symbol']
                except Exception as e:
                    print(f"Error using DexTools API: {str(e)}") # Keep incase response is useful for debugging in future.
            
            # Try alternative address formats (some APIs require lowercase)
            if price is None:
                try:
                    # Try lowercase address
                    alt_token_address = token_address.lower()
                    if alt_token_address != token_address:
                        alt_url = f"https://api.dexscreener.com/latest/dex/tokens/{alt_token_address}"
                        alt_response = requests.get(alt_url, timeout=10)
                        
                        if alt_response.status_code == 200:
                            alt_data = alt_response.json()
                            if alt_data and 'pairs' in alt_data and alt_data['pairs'] and len(alt_data['pairs']) > 0:
                                for pair in alt_data['pairs']:
                                    if 'chainId' in pair and pair['chainId'] == chain_id:
                                        price = float(pair['priceUsd'])
                                        # Get token info from the pair data
                                        if 'baseToken' in pair and pair['baseToken']['address'].lower() == alt_token_address:
                                            token_name = pair['baseToken'].get('name')
                                            token_symbol = pair['baseToken'].get('symbol')
                                            break
                                        elif 'quoteToken' in pair and pair['quoteToken']['address'].lower() == alt_token_address:
                                            token_name = pair['quoteToken'].get('name')
                                            token_symbol = pair['quoteToken'].get('symbol')
                                            break
                except Exception as alt_err:
                    print(f"Error trying alternative address format: {str(alt_err)}") # Keep incase response is useful for debugging in future.
            
            # If we found a price, update the cache
            if price is not None and price > 0:
                cache['token_prices'][cache_key] = price
                cache['last_price_update'][cache_key] = current_time
                # Store token info in cache
                if token_name and token_symbol:
                    cache_token_info_key = f"{chain_id}_{token_address}_info"
                    cache['token_prices'][cache_token_info_key] = {
                        'name': token_name,
                        'symbol': token_symbol
                    }
                return price, token_name, token_symbol
            else:
                # Return cached price if available, otherwise None
                return cache['token_prices'].get(cache_key, 1.0), None, None  # Default to 1.0 if no price available
            
        except Exception as e:
            print(f"Error in price fetching process: {str(e)}")  # Keep incase response is useful for debugging in future.
            # Return cached price if available, otherwise None
            return cache['token_prices'].get(cache_key, 1.0), None, None  # Default to 1.0 if no price available

def get_projects_and_chains():
    """Get list of available projects and chains"""
    if cache['projects'] is None or cache['chains'] is None:
        projects = {}
        chains = {}
        
        try:
            # Dummy config to initialize and get lists
            data = {
                "project_id": "basedfarm",  # Placeholder
                "wallet": "0x0000000000000000000000000000000000000000",  # Placeholder
                "strategy": "",
                "lp_summary": False,
                "parallel": False,
                "hide_no_rewards": False
            }
            
            # Fetch config data without printing
            def silent_print(*args, **kwargs):
                pass
            
            # Store original print function
            original_print = print
            
            # Temporarily replace print with silent version
            sys.stdout = open('nul', 'w') if sys.platform == 'win32' else open('/dev/null', 'w')
            
            # Load the configs - skip this step as it might be failing with missing projects
            # chain, project = config_fetcher.fetch_configs(data)
            
            # Restore stdout
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            
            # Get all projects
            projects = {}
            chains = {}
            sys.path.insert(0, 'config/projects/')
            import glob
            from importlib import reload
            
            for project_config_location in glob.glob("config/projects/*.py"):
                try:
                    filename = project_config_location.split("/")[-1].replace(".py", "")
                    project_module = __import__(filename)
                    reload(project_module)
                    projects[project_module.get_name()] = {
                        'name': project_module.get_name(),
                        'config': project_module.get_config()
                    }
                except Exception as e:
                    print(f'Failed to parse {project_config_location}: {e}')
                    traceback.print_exc()  # Add this to see the full error
                    
            # Continue only if we found at least one project
            if not projects:
                pass
                
            sys.path.insert(0, 'config/chains/')
            for chain_config_location in glob.glob("config/chains/*.py"):
                try:
                    filename = chain_config_location.split("/")[-1].replace(".py", "")
                    chain_module = __import__(filename)
                    reload(chain_module)
                    chains[chain_module.get_name()] = chain_module.get_config()
                except Exception as e:
                    print(f'Failed to parse {chain_config_location}: {e}')
                    
            # Update cache
            cache['projects'] = projects
            cache['chains'] = chains
            
        except Exception as e:
            print(f"Error loading projects and chains: {str(e)}") # Keep incase response is useful for debugging in future.
            print(traceback.format_exc()) # Keep incase response is useful for debugging in future.
            return {}, {}
            
    return cache['projects'], cache['chains']

@app.route('/')
def index():
    """Render the main dashboard page"""
    projects, chains = get_projects_and_chains()
    
    # Convert to format needed by template
    project_list = [
        {"id": project_id, "name": project_data['name']}
        for project_id, project_data in projects.items()
    ]
    
    # Sort projects alphabetically
    project_list.sort(key=lambda x: x["name"])
    
    return render_template('index.html', projects=project_list)

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    """Fetch project data based on form input"""
    try:
        data = request.json or {}
        
        project_id = data.get('project', 'hog')
        wallet = data.get('wallet', '0x81da1B2eeB44cb139C3B0643Dc10AbC2C0420003')
        strategy = data.get('strategy', '')
        lp_summary = data.get('lp_summary', False)
        parallel = data.get('parallel', False)
        hide_no_rewards = data.get('hide_no_rewards', False)
        manual_price = data.get('manual_price', None)  # Allow manually setting a price
            
        # Fetch the configuration
        try:
            chain, project = config_fetcher.fetch_configs({
                "project_id": project_id,
                "wallet": wallet,
                "strategy": strategy,
                "lp_summary": lp_summary,
                "parallel": parallel,
                "hide_no_rewards": hide_no_rewards
            })
        except Exception as config_error:
            print(f"Error loading project configuration: {str(config_error)}")
            print(traceback.format_exc())
            return jsonify({'error': f'Configuration error: {str(config_error)}'}), 500
        
        # Set manual price if provided
        if manual_price is not None and manual_price > 0:
            project['native_price'] = float(manual_price)
        
        # Fetch the project data
        try:
            fetched_project = project_fetcher.fetch_all(chain, project, wallet, strategy)
        except Exception as fetch_error:
            print(f"Error fetching project data: {str(fetch_error)}")
            print(traceback.format_exc())
            return jsonify({'error': f'Data fetch error: {str(fetch_error)}'}), 500
        
        if not fetched_project:
            print("Empty project data returned")
            return jsonify({'error': 'Failed to fetch project data - empty result'}), 500
        
        # Update token price from DexScreener if chain and token address are available
        chain_id = chain.get('chain_id', chain.get('name', ''))  # Use chain name as fallback
        if chain_id and 'native_token_address' in fetched_project:
            token_address = fetched_project['native_token_address']
            
            # Try to get updated price and token info
            price_data = get_token_price(chain_id, token_address)
            
            if isinstance(price_data, tuple) and len(price_data) >= 3:
                updated_price, token_name, token_symbol = price_data
            else:
                updated_price = price_data
                token_name = None
                token_symbol = None
                
            if updated_price is not None:
                # Update the price in the fetched project data
                old_price = fetched_project['native_price']
                fetched_project['native_price'] = updated_price
                
                # Update token name and symbol if available from API
                if token_name:
                    fetched_project['native_name'] = token_name
                if token_symbol:
                    fetched_project['native_symbol'] = token_symbol
                
                # Recalculate dollar rewards per second with new price
                if 'reward_rate' in fetched_project:
                    fetched_project['dollar_rewards_per_second'] = fetched_project['reward_rate'] * updated_price
                
                # Update pending rewards for each pool with the new price ratio
                price_ratio = updated_price / old_price if old_price > 0 else 1
                for pool in fetched_project['pools']:
                    if 'pending_rewards' in pool:
                        pool['pending_rewards'] = pool['pending_rewards'] * price_ratio
                
                # Update total pending rewards
                if 'total_pending' in fetched_project:
                    fetched_project['total_pending'] = fetched_project['total_pending'] * price_ratio

        # Calculate percentages for user pools
        user_pools = []
        for pool in fetched_project['pools']:
            if pool['user_value'] > 0:
                weight = pool['alloc_points'] / max(fetched_project['total_alloc_points'], 1)
                daily_rewards = weight * fetched_project['dollar_rewards_per_second'] * 60 * 60 * 24
                apr = 0
                if pool["tvl"] > 0:
                    apr = 365 * daily_rewards / pool["tvl"] * 100
                
                lp_info = None
                if lp_summary and all(key in pool for key in ['token0_amount', 'token0_symbol', 'token1_amount', 'token1_symbol']):
                    lp_info = {
                        'token0_amount': pool['token0_amount'],
                        'token0_symbol': pool['token0_symbol'],
                        'token1_amount': pool['token1_amount'],
                        'token1_symbol': pool['token1_symbol']
                    }
                
                user_pool = {
                    'pid': pool['pid'],
                    'token_name': pool['token_name'],
                    'token_address': pool['token_address'],
                    'token_symbol': pool['token_symbol'],
                    'tvl': pool['tvl'],
                    'apr': apr,
                    'user_value': pool['user_value'],
                    'weight': weight * 100,
                    'daily_rewards': daily_rewards,
                    'pending_rewards': pool.get('pending_rewards', 0),
                    'lp_info': lp_info
                }
                
                user_pools.append(user_pool)
        
        # Prepare response with relevant data
        response = {
            'project_name': fetched_project['project_name'],
            'native_name': fetched_project['native_name'],
            'native_symbol': fetched_project['native_symbol'],
            'native_price': fetched_project['native_price'],
            'native_token_address': fetched_project['native_token_address'],
            'mc_address': fetched_project['mc_address'],
            'reward_rate': fetched_project['reward_rate'],
            'dollar_rewards_per_second': fetched_project['dollar_rewards_per_second'],
            'total_value_locked': fetched_project['total_value_locked'],
            'total_deposit_value': fetched_project['total_deposit_value'],
            'total_pending': fetched_project.get('total_pending', 0),
            'all_pools': [{
                'pid': pool['pid'],
                'token_name': pool['token_name'],
                'token_address': pool['token_address'],
                'tvl': pool['tvl'],
                'apr': 365 * (pool['alloc_points'] / max(fetched_project['total_alloc_points'], 1)) * fetched_project['dollar_rewards_per_second'] * 60 * 60 * 24 / max(pool['tvl'], 1) * 100,
                'weight': (pool['alloc_points'] / max(fetched_project['total_alloc_points'], 1)) * 100,
                'daily_rewards': (pool['alloc_points'] / max(fetched_project['total_alloc_points'], 1)) * fetched_project['dollar_rewards_per_second'] * 60 * 60 * 24,
                'user_value': pool['user_value'],
                'pending_rewards': pool.get('pending_rewards', 0)
            } for pool in fetched_project['pools']],
            'user_pools': user_pools
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")  # Keep incase response is useful for debugging in future.
        print(traceback.format_exc()) # Keep incase response is useful for debugging in future.
        return jsonify({'error': str(e)}), 500

@app.route('/project-info/<project_id>')
def project_info(project_id):
    """Get info about a specific project (for strategy selection)"""
    projects, _ = get_projects_and_chains()
    
    if project_id not in projects:
        return jsonify({'error': 'Project not found'}), 404
        
    project_data = projects[project_id]
    
    # Check if the project has strategies
    strategies = project_data['config'].get('violin_strategy', {})
    
    return jsonify({
        'name': project_data['name'],
        'has_strategies': len(strategies) > 0,
        'strategies': [{'name': name, 'address': address} for name, address in strategies.items()]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)