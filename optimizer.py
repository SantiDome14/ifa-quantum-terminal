import numpy as np
import pandas as pd
from scipy.stats import norm

def calculate_advanced_metrics(returns, weights, risk_free_rate=0.0):
    """
    Calcula métricas avanzadas: VaR (95%), CVaR (95%) y Sortino Ratio.
    """
    # Retornos del portfolio
    portfolio_returns = returns.dot(weights)
    
    # VaR Paramétrico (95% trust)
    confidence_level = 0.95
    mean = np.mean(portfolio_returns)
    std_dev = np.std(portfolio_returns)
    var_95 = norm.ppf(1 - confidence_level, mean, std_dev)
    
    # Sortino Ratio
    # Solo consideramos la volatilidad negativa
    downside_returns = portfolio_returns[portfolio_returns < 0]
    downside_std = np.std(downside_returns)
    
    expected_return = np.sum(returns.mean() * weights) * 252
    sortino = (expected_return - risk_free_rate) / (downside_std * np.sqrt(252))
    
    return var_95, sortino

def monte_carlo_simulation(data, risk_free_rate, n_simulations=5000, min_weight=0.0, max_weight=1.0):
    """
    Ejecuta simulaciones de portafolio respetando restricciones de peso.
    """
    log_returns = np.log(data / data.shift(1))
    cov_matrix = log_returns.cov() * 252
    
    results_list = []
    weights_list = []
    tickers = data.columns
    num_assets = len(tickers)
    
    
    attempts = 0
    valid_simulations = 0
    max_attempts = n_simulations * 5
    
    while valid_simulations < n_simulations and attempts < max_attempts:
        attempts += 1
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        
        if np.any(weights < min_weight) or np.any(weights > max_weight):
            continue
            
        valid_simulations += 1
        
        mean_returns = log_returns.mean() * 252 
        portfolio_return = np.sum(mean_returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
        
        results_list.append([portfolio_return, portfolio_volatility, sharpe_ratio])
        weights_list.append(weights)

    columns = ['Retorno', 'Volatilidad', 'Sharpe_Ratio']
    results_df = pd.DataFrame(results_list, columns=columns)
    weights_df = pd.DataFrame(weights_list, columns=tickers)
    final_df = pd.concat([results_df, weights_df], axis=1)
    
    if final_df.empty:
        return pd.DataFrame(), None, None

    max_sharpe_idx = final_df['Sharpe_Ratio'].idxmax()
    min_vol_idx = final_df['Volatilidad'].idxmin()
    
    max_sharpe_port = final_df.loc[max_sharpe_idx]
    min_vol_port = final_df.loc[min_vol_idx]
    
    final_df['Tipo'] = 0
    final_df.loc[max_sharpe_idx, 'Tipo'] = 1 
    final_df.loc[min_vol_idx, 'Tipo'] = 2 
    
    return final_df, max_sharpe_port, min_vol_port

def create_correlation_matrix(data):
    return data.pct_change().corr()