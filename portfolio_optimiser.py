import pandas as pd
import numpy as np
from scipy.optimize import minimize

def optimize_portfolio(data, risk_tolerance):
    """
    Performs Modern Portfolio Theory (MPT) optimization with diversification constraints.

    Args:
        data (pandas.DataFrame): DataFrame containing historical stock prices.
        risk_tolerance (float): Risk tolerance level (higher value means higher risk).

    Returns:
        dict: Dictionary containing optimized asset weights for a diversified portfolio.
    """
    try:
        # Calculate daily returns & covariance matrix
        returns = data.pct_change().dropna()
        mean_returns = returns.mean()
        cov_matrix = returns.cov()

        num_assets = len(mean_returns)
        risk_free_rate = 0.01  # Example: Assume a 1% risk-free rate

        # Objective Function: Maximize Sharpe Ratio
        def negative_sharpe_ratio(weights):
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std_dev
            return -sharpe_ratio

        # Constraints:
        constraints = [
            {"type": "eq", "fun": lambda x: np.sum(x) - 1},  # Sum of weights must be 1
        ]

        # Set Diversification Constraints
        max_allocation = 0.50  # Max 50% allocation per asset
        min_assets_allocated = 2  # At least 2 assets must have nonzero allocation

        def diversification_constraint(weights):
            return np.count_nonzero(weights) - min_assets_allocated  # Enforce minimum assets

        constraints.append({"type": "ineq", "fun": diversification_constraint})

        # Set Bounds (Per-Asset Allocation Limits)
        bounds = tuple((0.05, max_allocation) for _ in range(num_assets))  # Min 5%, Max 50%

        # Initialise Equal Weights
        initial_weights = np.array([1 / num_assets] * num_assets)

        # Optimise Portfolio Allocation
        optimized_results = minimize(
            negative_sharpe_ratio,
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        # Extract Optimal Weights
        asset_weights = dict(zip(data.columns, optimized_results.x))
        return asset_weights

    except Exception as e:
        print(f"Error optimizing portfolio: {e}")
        return None
