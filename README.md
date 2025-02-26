# CarlosScan

A comprehensive DeFi analytics tool for fetching and displaying project details, including pool information, TVL, APR, and user positions across multiple blockchains and protocols.

## Overview

CarlosScan provides both a web dashboard and command-line interface for:
- Tracking your DeFi positions across various protocols
- Viewing pool information including TVL, APR, and rewards
- Analyzing LP token compositions
- Monitoring pending rewards
- Calculating earnings projections

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/CarlosScan.git
   cd CarlosScan
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. (Optional) Configure environment variables for price APIs:
   ```
   # For DexTools API (optional)
   export DEXTOOLS_API_KEY="your_api_key_here"
   
   # Default DexScreener API URL can be customized if needed
   export DEXSCREENER_API_URL="https://api.dexscreener.com/latest/dex/pairs"
   ```

## Web Dashboard Usage

### Starting the Server

Launch the web dashboard with:
```
python app.py
```

Then access the dashboard at [http://localhost:5050](http://localhost:5050) in your browser.

### Dashboard Features

1. **Project Selection**:
   - Choose from available DeFi projects/protocols
   - Each project connects to the corresponding blockchain

2. **Strategy Selection**:
   - Some projects offer predefined strategy options
   - Select from available strategies or use a custom wallet address

3. **Wallet Configuration**:
   - Enter the wallet address to analyze
   - Track positions and rewards for the specified wallet

4. **Display Options**:
   - Include LP Summary: Shows breakdown of LP token compositions
   - Enable Parallel Fetching: Speed up data retrieval for projects with many pools
   - Hide No Rewards: Filter out pools without active rewards
   - Override Token Price: Manually set token prices for analysis

5. **Auto-refresh**:
   - Enable periodic data refreshing (every 60 seconds)
   - Keep reward and pricing data current

6. **Data Views**:
   - Project Overview: Token price, TVL, reward rates
   - Your Pools: Pools where you have active positions
   - All Available Pools: Complete listing of project pools

## Command-Line Usage

### Basic Syntax

```
python main.py PROJECT_ID WALLET_ADDRESS [options]
```

### Required Arguments

- `PROJECT_ID`: Identifier for the project (e.g., 'hog', 'aerodrome', 'baseswap')
- `WALLET_ADDRESS`: The wallet address to analyze (EVM-compatible address)

### Options

- `--strategy STRATEGY`: Use a predefined strategy from the project config
- `--lp_summary`: Include detailed LP token composition data
- `--parallel`: Enable parallel processing for faster data retrieval
- `--hide_no_rewards`: Hide pools that don't have active rewards

### Examples

1. Basic project query:
   ```
   python main.py hog 0x81da1B2eeB44cb139C3B0643Dc10AbC2C0420003
   ```

2. Using a strategy with LP breakdown:
   ```
   python main.py hog 0x81da1B2eeB44cb139C3B0643Dc10AbC2C0420003 --strategy carlos --lp_summary
   ```

3. Fetch all pools with parallel processing:
   ```
   python main.py hog 0x81da1B2eeB44cb139C3B0643Dc10AbC2C0420003 --parallel
   ```

## Configuration

### Project Configuration

Projects are defined in Python files located in the `config/projects/` directory:

- Each project has its own configuration file (e.g., `hog.py`, `baseswap.py`)
- Configuration includes masterchef addresses, token addresses, and other protocol-specific settings
- Optional strategy configurations for predefined wallet addresses

Example project configuration:
```python
config = {
    "name": "projectname",
    "chain": "chainname",           # Must match a chain config file name
    "mc_address": "0x123...",       # Masterchef contract address
    "native_token_address": "0x456...",
    "reward_rate_function": "rewardPerSecond()",
    "pending_rewards_function": "pendingReward(uint256,address)",
    "allocPoints": 2,               # Position of allocPoints in poolInfo
    "rewards_per_second": True,     # True for per-second, False for per-block
    "native_price": 1.0,            # Default price (will be updated from API)
    "native_decimals": 18,
    "violin_strategy": {
        "strategy1": "0x789...",    # Strategy wallet addresses
        "strategy2": "0xabc..."
    },
    "mc_abi": '[...]'               # Masterchef ABI
}
```

### Chain Configuration

Chain configurations are in `config/chains/` directory:

- Each chain has a dedicated config file (e.g., `eth.py`, `sonic.py`)
- Configurations include RPC endpoints, block intervals, and chain identifiers
- Use the appropriate chain ID for price fetching

Example chain configuration:
```python
config = {
    "name": "sonic",
    "chain_id": "sonic",            # Chain ID for price API lookup
    "pricer": "0x7FA4b073...",      # Price oracle contract
    "rpc": "https://rpc.example.com",
    "explorer": "https://explorer.example.com",
    "block_interval": 0.3           # Average block time in seconds
}
```

### Portfolio Configuration

Portfolio configurations are in the `config/portfolios/` directory:

- Define collections of wallets to analyze together
- Easy tracking of multiple addresses in one query

## Price Fetching

CarlosScan fetches token prices from:

1. DexScreener API (default)
2. DexTools API (if configured with API key)
3. Fallback to manual price input on the dashboard

Price caching is implemented to reduce API calls, with a refresh interval of 3 minutes.

## Troubleshooting

### Common Issues

1. **RPC Connection Errors**:
   - Verify the RPC endpoint in the chain configuration
   - Try an alternative RPC provider for the chain

2. **Missing Pool Data**:
   - Check that the masterchef address and ABI are correct
   - Confirm that the project is still active and pools are available

3. **Price Fetch Failures**:
   - Try enabling manual price override
   - Check that the token address is correct and the token is listed on DEXes

4. **Web3.py Version Compatibility**:
   - The tool supports both legacy and newer web3.py versions
   - If you encounter address checksumming errors, check your web3.py version

### Debugging

For more verbose output when troubleshooting:

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Features

### Parallel Processing

For projects with many pools, enable parallel processing to speed up data retrieval:

```
python main.py project_id wallet_address --parallel
```

### Custom Price Oracles

The system supports custom price oracles by specifying the `pricer` address in chain configs.

### Strategy Analysis

Many projects include predefined strategies that can be analyzed without knowing the wallet address:

```
python main.py project_id dummy_address --strategy strategy_name
```

## License

This project is available under the [MIT License](https://opensource.org/licenses/MIT).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.