# CarlosScan

A command-line tool for fetching and displaying DeFi project details, including pool information, TVL, APR, and user stakes.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/CarlosScan.git
   cd CarlosScan
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Basic usage:
```
python main.py PROJECT_ID WALLET_ADDRESS [options]
```

### Arguments

- `PROJECT_ID`: The ID of the project to query (e.g., 'aerodrome', 'basedfarm')
- `WALLET_ADDRESS`: The wallet address to check positions for

### Options

- `--strategy STRATEGY`: Use a predefined strategy name (from the project config)
- `--lp_summary`: Include LP token composition details
- `--parallel`: Enable parallel processing of pool data
- `--hide_no_rewards`: Hide pools with no rewards

### Examples

1. Basic query:
   ```
   python main.py aerodrome 0x1119C4ce8F56d96a51b5A38260Fede037C7126F5
   ```

2. With LP summary:
   ```
   python main.py basedfarm 0x1119C4ce8F56d96a51b5A38260Fede037C7126F5 --lp_summary
   ```

3. Using a strategy with parallel processing:
   ```
   python main.py aerodrome 0x1119C4ce8F56d96a51b5A38260Fede037C7126F5 --strategy carlos --parallel
   ```

## Project Configuration

Projects are configured in the `config/projects/` directory. Each project has its own Python file with a configuration dictionary.

## Chain Configuration

Chain configurations are in the `config/chains/` directory. Each supported blockchain has its own Python file with RPC URLs and other chain-specific settings.