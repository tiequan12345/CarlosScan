document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const queryForm = document.getElementById('queryForm');
    const projectSelect = document.getElementById('projectSelect');
    const strategySelect = document.getElementById('strategySelect');
    const strategySelectContainer = document.getElementById('strategySelectContainer');
    const walletInput = document.getElementById('walletInput');
    const lpSummaryCheck = document.getElementById('lpSummaryCheck');
    const parallelCheck = document.getElementById('parallelCheck');
    const hideNoRewardsCheck = document.getElementById('hideNoRewardsCheck');
    const fetchButton = document.getElementById('fetchButton');
    
    // Display areas
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorDisplay = document.getElementById('errorDisplay');
    const errorMessage = document.getElementById('errorMessage');
    const resultsArea = document.getElementById('resultsArea');
    
    // Result elements
    const projectName = document.getElementById('projectName');
    const nativeTokenInfo = document.getElementById('nativeTokenInfo');
    const tokenPrice = document.getElementById('tokenPrice');
    const totalTvl = document.getElementById('totalTvl');
    const rewardRate = document.getElementById('rewardRate');
    const totalUserValue = document.getElementById('totalUserValue');
    const userPoolsBody = document.getElementById('userPoolsBody');
    const noUserPools = document.getElementById('noUserPools');
    const allPoolsBody = document.getElementById('allPoolsBody');
    
    // When project changes, check if it has strategies
    projectSelect.addEventListener('change', function() {
        const projectId = this.value;
        if (!projectId) return;
        
        // Clear strategy select
        strategySelect.innerHTML = '<option value="" selected>None (use wallet)</option>';
        strategySelectContainer.style.display = 'none';
        
        // Fetch project info to check for strategies
        fetch(`/project-info/${projectId}`)
            .then(response => response.json())
            .then(data => {
                if (data.has_strategies && data.strategies && data.strategies.length > 0) {
                    // Populate strategies dropdown
                    data.strategies.forEach(strategy => {
                        const option = document.createElement('option');
                        option.value = strategy.name;
                        option.textContent = strategy.name;
                        strategySelect.appendChild(option);
                    });
                    
                    strategySelectContainer.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error fetching project info:', error);
            });
    });
    
    // Form submission
    queryForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        if (!projectSelect.value) {
            alert('Please select a project');
            return;
        }
        
        if (!walletInput.value) {
            alert('Please enter a wallet address');
            return;
        }
        
        // Show loading indicator, hide other areas
        loadingIndicator.classList.remove('d-none');
        errorDisplay.classList.add('d-none');
        resultsArea.classList.add('d-none');
        
        // Disable the fetch button during request
        fetchButton.disabled = true;
        
        // Prepare the request data
        const requestData = {
            project: projectSelect.value,
            wallet: walletInput.value,
            strategy: strategySelect.value || '',
            lp_summary: lpSummaryCheck.checked,
            parallel: parallelCheck.checked,
            hide_no_rewards: hideNoRewardsCheck.checked
        };
        
        // Fetch the data
        fetch('/fetch-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Unknown error occurred');
                });
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator, show results
            loadingIndicator.classList.add('d-none');
            resultsArea.classList.remove('d-none');
            
            // Display project overview
            displayProjectOverview(data);
            
            // Display user pools
            displayUserPools(data.user_pools, data.lp_summary);
            
            // Display all pools
            displayAllPools(data.all_pools);
        })
        .catch(error => {
            // Hide loading indicator, show error
            loadingIndicator.classList.add('d-none');
            errorDisplay.classList.remove('d-none');
            
            errorMessage.textContent = error.message || 'Failed to fetch data';
            console.error('Error:', error);
        })
        .finally(() => {
            // Re-enable the fetch button
            fetchButton.disabled = false;
        });
    });
    
    function displayProjectOverview(data) {
        projectName.textContent = data.project_name;
        nativeTokenInfo.textContent = `${data.native_name} (${data.native_symbol})`;
        tokenPrice.textContent = `$${formatNumber(data.native_price)}`;
        totalTvl.textContent = `$${formatNumber(data.total_value_locked)}`;
        rewardRate.textContent = `${formatNumber(data.reward_rate, 4)} ${data.native_symbol}/sec ($${formatNumber(data.dollar_rewards_per_second)}/sec)`;
        totalUserValue.textContent = `$${formatNumber(data.total_deposit_value)}`;
    }
    
    function displayUserPools(pools, includeLpSummary) {
        userPoolsBody.innerHTML = '';
        
        if (!pools || pools.length === 0) {
            // Show no pools message
            noUserPools.classList.remove('d-none');
            return;
        }
        
        // Hide no pools message
        noUserPools.classList.add('d-none');
        
        // Add user pools to table
        pools.forEach(pool => {
            const row = document.createElement('tr');
            
            // Determine APR color
            let aprClass = '';
            if (pool.apr > 100) aprClass = 'badge-apr-high';
            else if (pool.apr > 50) aprClass = 'badge-apr-medium';
            else aprClass = 'badge-apr-low';
            
            row.innerHTML = `
                <td>${pool.pid}</td>
                <td>
                    ${pool.token_name}
                    ${pool.lp_info ? `<div class="lp-details">${formatNumber(pool.lp_info.token0_amount)} ${pool.lp_info.token0_symbol} and ${formatNumber(pool.lp_info.token1_amount)} ${pool.lp_info.token1_symbol}</div>` : ''}
                </td>
                <td>$${formatNumber(pool.tvl)}</td>
                <td><span class="badge ${aprClass}">${formatNumber(pool.apr)}%</span></td>
                <td>$${formatNumber(pool.daily_rewards)}</td>
                <td>$${formatNumber(pool.user_value)}</td>
                <td>$${formatNumber(pool.pending_rewards)}</td>
            `;
            
            userPoolsBody.appendChild(row);
        });
    }
    
    function displayAllPools(pools) {
        allPoolsBody.innerHTML = '';
        
        // Sort pools by TVL descending
        pools.sort((a, b) => b.tvl - a.tvl);
        
        // Add all pools to table
        pools.forEach(pool => {
            const row = document.createElement('tr');
            
            // Determine APR color
            let aprClass = '';
            if (pool.apr > 100) aprClass = 'badge-apr-high';
            else if (pool.apr > 50) aprClass = 'badge-apr-medium';
            else aprClass = 'badge-apr-low';
            
            row.innerHTML = `
                <td>${pool.pid}</td>
                <td>${pool.token_name}</td>
                <td>$${formatNumber(pool.tvl)}</td>
                <td>${formatNumber(pool.weight, 1)}%</td>
                <td><span class="badge ${aprClass}">${formatNumber(pool.apr)}%</span></td>
                <td>$${formatNumber(pool.daily_rewards)}</td>
            `;
            
            // Highlight user's pools
            if (pool.user_value > 0) {
                row.classList.add('bg-light');
            }
            
            allPoolsBody.appendChild(row);
        });
    }
    
    function formatNumber(value, decimals = 2) {
        if (value === null || value === undefined) return '0';
        
        // Format with specified decimal places
        const formatted = Number(value).toLocaleString(undefined, {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
        
        return formatted;
    }
    
    // Optional: Load from localStorage
    const savedWallet = localStorage.getItem('carlosScan_wallet');
    if (savedWallet) {
        walletInput.value = savedWallet;
    }
    
    // Save wallet address to localStorage when entered
    walletInput.addEventListener('change', function() {
        localStorage.setItem('carlosScan_wallet', this.value);
    });
});