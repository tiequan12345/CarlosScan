def print_details(project):
    # Output our data to the dashboard
    print(f"Masterchef {project['mc_address']} details for {project['project_name']}:")
    print(f"{project['native_name']} ({project['native_token_address']}): ${project['native_price']:.2f}")
    print(f"Reward rate: {project['reward_rate']:.4f} {project['native_symbol']}/second")
    print(f"Reward rate: ${project['dollar_rewards_per_second']:.2f}/second")
    print("")
    print(f"{len(project['pools'])} pools (${project['total_value_locked']:,.0f} TVL):")
    print("")
    
    # Show all pools
    for pool in project['pools']:
        weight = pool['alloc_points'] / max(project['total_alloc_points'], 1)  # Avoid division by zero
        daily_rewards = weight * project['dollar_rewards_per_second'] * 60 * 60 * 24
        apr = 0
        if pool["tvl"] > 0:
            apr = 365 * daily_rewards / pool["tvl"] * 100
        
        print(f'{pool["pid"]}: {pool["token_name"]} ({weight*100:.0f}%) - TVL: ${pool["tvl"]:,.0f} - DAILY: ${daily_rewards:,.0f} - APR: {apr:,.2f}% - User stake: ${pool["user_value"]:,.2f} - Pending rewards: ${pool.get("pending_rewards", 0):,.2f} - ${pool["token_address"]}')
    
    # Show only user's pools
    print("")
    print("Your pools:")
    user_pools = [p for p in project['pools'] if p['user_value'] > 0]
    
    if not user_pools:
        print("No active pools found for this wallet.")
    else:
        for pool in user_pools:
            weight = pool['alloc_points'] / max(project['total_alloc_points'], 1)  # Avoid division by zero
            daily_rewards = weight * project['dollar_rewards_per_second'] * 60 * 60 * 24
            apr = 0
            if pool["tvl"] > 0:
                apr = 365 * daily_rewards / pool["tvl"] * 100
                
            line = f'{pool["pid"]}: {pool["token_name"]} - TVL: ${pool["tvl"]:,.0f} - APR: {apr:,.2f}% - User stake: ${pool["user_value"]:,.2f}'
            
            # Add LP details if available
            if project.get('lp_summary', False) and all(key in pool for key in ['token0_amount', 'token0_symbol', 'token1_amount', 'token1_symbol']):
                line += f' ({pool["token0_amount"]:,.2f} {pool["token0_symbol"]} and {pool["token1_amount"]:,.2f} {pool["token1_symbol"]})'
                
            print(line)
    
    print("")
    print(f"Total deposits: ${project['total_deposit_value']:,.2f}")
    
    if project['total_pending'] > 0:
        print(f"Total pending rewards: ${project['total_pending']:,.2f}")