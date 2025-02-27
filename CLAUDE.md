# CarlosScan Development Guide

## Commands
- Run web dashboard: `python app.py` (runs on http://localhost:5050)
- Run CLI tool: `python main.py <PROJECT_ID> <WALLET_ADDRESS> [options]`
  - Options: `--strategy <STRATEGY>` `--lp_summary` `--parallel` `--hide_no_rewards`
- No formal test commands found in the repository

## Code Style
- **Indentation**: 4 spaces for most files, 2 spaces seen in some files like config_fetcher.py
- **Imports**: Standard library first, then project imports, no specific sorting
- **Naming**: snake_case for functions/variables, UPPER_SNAKE_CASE for constants
- **Error handling**: 
  - Use try/except with specific exceptions when possible
  - Print error messages with traceback for debugging
  - Gracefully fallback to defaults when errors occur
- **Comments**: Use docstrings for functions, inline comments for complex logic

## Architecture
- Configuration-driven design with separate modules for chains, projects, and portfolios
- Comprehensive error handling and fallbacks for API calls
- Price caching with time-based invalidation (3 minutes default)
- Parallel fetching capabilities for performance optimization