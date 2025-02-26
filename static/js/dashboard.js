// Add event handlers once the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch project data
    window.fetchProjectData = function(showLoading = true, manualPrice = null) {
        const project = document.getElementById('projectSelect').value;
        const wallet = document.getElementById('walletInput').value;
        const strategy = document.getElementById('strategySelect').value;
        const lpSummary = document.getElementById('lpSummaryCheck').checked;
        const hideNoRewards = document.getElementById('hideNoRewardsCheck').checked;
        const parallelFetch = document.getElementById('parallelCheck').checked;
        
        // Use manual price from form field if not explicitly provided
        if (manualPrice === null) {
            const manualPriceInput = document.getElementById('manualPriceInput');
            if (manualPriceInput && manualPriceInput.value) {
                manualPrice = parseFloat(manualPriceInput.value);
                if (isNaN(manualPrice) || manualPrice <= 0) {
                    manualPrice = null;
                }
            }
        }
        
        if (manualPrice) {
            console.log(`Using manual price: $${manualPrice}`);
        }
        
        // Show loading indicator
        if (showLoading) {
            document.getElementById('loadingIndicator').classList.remove('d-none');
            document.getElementById('resultsArea').classList.add('d-none');
            document.getElementById('errorDisplay').classList.add('d-none');
        }
        
        fetch('/fetch-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                project: project,
                wallet: wallet,
                strategy: strategy,
                lp_summary: lpSummary,
                hide_no_rewards: hideNoRewards,
                parallel: parallelFetch,
                manual_price: manualPrice
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            document.getElementById('loadingIndicator').classList.add('d-none');
            
            if (data.error) {
                document.getElementById('errorDisplay').classList.remove('d-none');
                document.getElementById('errorMessage').textContent = data.error;
                return;
            }
            
            updateDashboard(data);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loadingIndicator').classList.add('d-none');
            document.getElementById('errorDisplay').classList.remove('d-none');
            document.getElementById('errorMessage').textContent = `Failed to fetch data: ${error.message}`;
        });
    };
    
    // Attach form submit handler
    document.getElementById('queryForm').addEventListener('submit', function(e) {
        e.preventDefault();
        fetchProjectData();
    });
    
    // Add manual price input functionality
    const manualPriceContainer = document.createElement('div');
    manualPriceContainer.className = 'mb-3';
    manualPriceContainer.innerHTML = `
        <label for="manual-price" class="form-label">Override Token Price (USD):</label>
        <div class="input-group">
            <span class="input-group-text">$</span>
            <input type="number" class="form-control" id="manual-price" placeholder="Enter price" step="0.000001" min="0">
            <button class="btn btn-primary" type="button" id="apply-price">Apply</button>
        </div>
        <small class="form-text text-muted">Leave empty to use API price.</small>
    `;
    
    // Insert after the wallet input
    const walletInput = document.querySelector('#walletInput');
    if (walletInput) {
        walletInput.closest('.mb-3').after(manualPriceContainer);
    }
    
    // Button to apply manual price
    document.getElementById('apply-price').addEventListener('click', function() {
        const manualPrice = parseFloat(document.getElementById('manual-price').value);
        if (!isNaN(manualPrice) && manualPrice > 0) {
            // Re-fetch data with manual price
            fetchProjectData(true, manualPrice);
        }
    });
    
    // Auto-refresh functionality
    let autoRefreshInterval = null;
    
    // Add auto-refresh toggle
    const refreshContainer = document.createElement('div');
    refreshContainer.className = 'form-check mb-3';
    refreshContainer.innerHTML = `
        <input class="form-check-input" type="checkbox" id="auto-refresh">
        <label class="form-check-label" for="auto-refresh">
            Auto-refresh data (every 60 seconds)
        </label>
    `;
    
    // Insert before the submit button
    const submitButton = document.querySelector('#fetchButton');
    if (submitButton) {
        submitButton.closest('.mb-3').before(refreshContainer);
    }
    
    // Auto-refresh toggle handler
    document.getElementById('auto-refresh').addEventListener('change', function() {
        if (this.checked) {
            // Start auto-refresh
            autoRefreshInterval = setInterval(() => {
                const manualPrice = parseFloat(document.getElementById('manual-price').value);
                fetchProjectData(false, !isNaN(manualPrice) && manualPrice > 0 ? manualPrice : null);
            }, 60000); // Every 60 seconds
        } else {
            // Stop auto-refresh
            if (autoRefreshInterval) {
                clearInterval(autoRefreshInterval);
                autoRefreshInterval = null;
            }
        }
    });
    
    // Function to update dashboard with fetched data
    function updateDashboard(data) {
        // Format numbers with commas
        const formatter = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        
        const percentFormatter = new Intl.NumberFormat('en-US', {
            style: 'percent',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        
        // Show results area
        document.getElementById('resultsArea').classList.remove('d-none');
        
        // Update project overview card
        document.getElementById('projectName').textContent = data.project_name;
        document.getElementById('nativeTokenInfo').textContent = `${data.native_name} (${data.native_symbol})`;
        document.getElementById('tokenPrice').textContent = formatter.format(data.native_price);
        document.getElementById('totalTvl').textContent = formatter.format(data.total_value_locked);
        document.getElementById('rewardRate').textContent = `${data.reward_rate.toFixed(4)} ${data.native_symbol}/second (${formatter.format(data.dollar_rewards_per_second)}/second)`;
        document.getElementById('totalUserValue').textContent = formatter.format(data.total_deposit_value);
        
        // Update user pools
        const userPoolsBody = document.getElementById('userPoolsBody');
        userPoolsBody.innerHTML = '';
        
        if (data.user_pools && data.user_pools.length > 0) {
            document.getElementById('noUserPools').classList.add('d-none');
            document.getElementById('userPoolsTable').classList.remove('d-none');
            
            data.user_pools.forEach(pool => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${pool.pid}</td>
                    <td>${pool.token_name}</td>
                    <td>${formatter.format(pool.tvl)}</td>
                    <td>${pool.apr.toFixed(2)}%</td>
                    <td>${formatter.format(pool.daily_rewards)}</td>
                    <td>${formatter.format(pool.user_value)}</td>
                    <td>${formatter.format(pool.pending_rewards || 0)}</td>
                `;
                userPoolsBody.appendChild(row);
                
                // Add LP breakdown if available
                if (pool.lp_info) {
                    const lpRow = document.createElement('tr');
                    lpRow.className = 'table-light small';
                    lpRow.innerHTML = `
                        <td colspan="7" class="text-muted">
                            LP Breakdown: ${pool.lp_info.token0_amount.toFixed(4)} ${pool.lp_info.token0_symbol} and
                            ${pool.lp_info.token1_amount.toFixed(4)} ${pool.lp_info.token1_symbol}
                        </td>
                    `;
                    userPoolsBody.appendChild(lpRow);
                }
            });
        } else {
            document.getElementById('noUserPools').classList.remove('d-none');
            document.getElementById('userPoolsTable').classList.add('d-none');
        }
        
        // Update all pools
        const allPoolsBody = document.getElementById('allPoolsBody');
        allPoolsBody.innerHTML = '';
        
        data.all_pools.forEach(pool => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${pool.pid}</td>
                <td>${pool.token_name}</td>
                <td>${formatter.format(pool.tvl)}</td>
                <td>${pool.weight.toFixed(2)}%</td>
                <td>${pool.apr.toFixed(2)}%</td>
                <td>${formatter.format(pool.daily_rewards)}</td>
            `;
            allPoolsBody.appendChild(row);
        });
    }
    
    // Handle project change for strategies
    document.getElementById('projectSelect').addEventListener('change', function() {
        const projectId = this.value;
        const strategySelect = document.getElementById('strategySelect');
        const strategyContainer = document.getElementById('strategySelectContainer');
        
        // Reset strategy dropdown
        strategySelect.innerHTML = '<option value="">None (use wallet)</option>';
        strategyContainer.style.display = 'none';
        
        // Fetch project info
        fetch(`/project-info/${projectId}`)
            .then(response => response.json())
            .then(data => {
                if (data.has_strategies) {
                    strategyContainer.style.display = 'block';
                    data.strategies.forEach(strategy => {
                        const option = document.createElement('option');
                        option.value = strategy.name;
                        option.textContent = strategy.name;
                        strategySelect.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching project info:', error);
            });
    });
});