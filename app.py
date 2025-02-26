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
    
    with price_lock:
        current_time = time.time()
        # Check if we have a cached price that's still fresh
        if (cache_key in cache['token_prices'] and 
            cache_key in cache['last_price_update'] and
            current_time - cache['last_price_update'][cache_key] < PRICE_UPDATE_INTERVAL):
            print(f"Using cached price for {token_address}: ${cache['token_prices'][cache_key]}")
            return cache['token_prices'][cache_key]
        
        # If not, fetch new price
        try:
            dexscreener_api_url = os.environ.get("DEXSCREENER_API_URL", "https://api.dexscreener.com/latest/dex/pairs")
            url = f"{dexscreener_api_url}/{chain_id}/{token_address}"
            print(f"Fetching price from {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'pairs' in data and data['pairs'] and len(data['pairs']) > 0:
                    price = float(data['pairs'][0]['priceUsd'])
                    print(f"Got new price for {token_address}: ${price}")
                    # Update cache
                    cache['token_prices'][cache_key] = price
                    cache['last_price_update'][cache_key] = current_time
                    return price
            
            # If we get here, something went wrong with the API call
            print(f"Failed to get price for {token_address} on {chain_id}: {response.status_code}")
            # Return cached price if available, otherwise None
            return cache['token_prices'].get(cache_key)
            
        except Exception as e:
            print(f"Error fetching token price: {str(e)}")
            # Return cached price if available, otherwise None
            return cache['token_prices'].get(cache_key)

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
                print("Warning: No valid projects found in config/projects/")
                
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
            print(f"Error loading projects and chains: {str(e)}")
            print(traceback.format_exc())
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
        data = request.json
        project_id = data.get('project')
        wallet = data.get('wallet')
        strategy = data.get('strategy', '')
        lp_summary = data.get('lp_summary', False)
        parallel = data.get('parallel', False)
        hide_no_rewards = data.get('hide_no_rewards', False)
        
        if not project_id or not wallet:
            return jsonify({'error': 'Missing required parameters'}), 400
            
        # Fetch the configuration
        chain, project = config_fetcher.fetch_configs({
            "project_id": project_id,
            "wallet": wallet,
            "strategy": strategy,
            "lp_summary": lp_summary,
            "parallel": parallel,
            "hide_no_rewards": hide_no_rewards
        })
        
        # Fetch the project data
        fetched_project = project_fetcher.fetch_all(chain, project, wallet, strategy)
        
        if not fetched_project:
            return jsonify({'error': 'Failed to fetch project data'}), 500
        
        # Update token price from DexScreener if chain and token address are available
        if 'chain_id' in chain and 'native_token_address' in fetched_project:
            chain_id = chain['chain_id']
            token_address = fetched_project['native_token_address']
            
            print(f"Before price update: native_price = ${fetched_project['native_price']}")
            
            # Try to get updated price
            updated_price = get_token_price(chain_id, token_address)
            if updated_price is not None:
                # Update the price in the fetched project data
                print(f"Updating native_price from ${fetched_project['native_price']} to ${updated_price}")
                fetched_project['native_price'] = updated_price
                
                # Recalculate dollar rewards per second with new price
                if 'reward_rate' in fetched_project:
                    old_dollar_rewards = fetched_project['dollar_rewards_per_second']
                    fetched_project['dollar_rewards_per_second'] = fetched_project['reward_rate'] * updated_price
                    print(f"Updated dollar_rewards_per_second from ${old_dollar_rewards} to ${fetched_project['dollar_rewards_per_second']}")
            else:
                print("Failed to get updated price, using existing price")
        else:
            print("Missing chain_id or native_token_address, cannot update price")
            if 'chain_id' not in chain:
                print("Missing chain_id")
            if 'native_token_address' not in fetched_project:
                print("Missing native_token_address")
        
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
        print(f"Error processing request: {str(e)}")
        print(traceback.format_exc())
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