import numpy as np
import pandas as pd

BESS_CAPACITY = 50  # MWh
MAX_C_RATE = 0.5    # 0.5C (Max charge/discharge rate is 25 MW)
RT_AFRR_PRICE = 250 # €/MWh for aFRR service delivery
DA_ARBITRAGE_THRESHOLD = 0.1


def generate_stochastic_scenarios(base_prices, num_scenarios=10, vol_factor=0.15):
    """
    Generates probabilistic DA and RT price paths for a 24-hour horizon.

    Args:
        base_prices (np.array): Base DA price forecast.
        num_scenarios (int): Number of Monte Carlo scenarios.
        vol_factor (float): Volatility factor for RT price noise.

    Returns:
        pd.DataFrame: Columns DA_Price_sN and RT_Price_sN for each scenario N,
                      plus a Probability column (equal weights).
    """
    HOURS = len(base_prices)
    scenarios = pd.DataFrame(index=pd.to_datetime(np.arange(HOURS), unit='h'))

    NE_FORECAST_ERROR_DRIVER = base_prices.mean() * 0.1

    for s in range(num_scenarios):
        da_noise = np.random.normal(0, base_prices.mean() * vol_factor * 0.2, base_prices.shape)
        da_price_s = np.maximum(5, base_prices + da_noise)
        scenarios[f'DA_Price_s{s}'] = da_price_s

        ne_error = np.random.normal(0, 1, HOURS)
        rt_price_volatility = NE_FORECAST_ERROR_DRIVER * ne_error * vol_factor
        rt_price_s = np.maximum(5, da_price_s + rt_price_volatility)
        scenarios[f'RT_Price_s{s}'] = rt_price_s

    scenarios['Probability'] = 1 / num_scenarios
    return scenarios


def solve_scenario_optimization(scenarios, capacity_reserved_rt):
    """
    Stage-2 dispatch: for each scenario, compute DA arbitrage profit plus
    fixed aFRR revenue for the reserved capacity.

    Args:
        scenarios (pd.DataFrame): Output of generate_stochastic_scenarios.
        capacity_reserved_rt (float): MWh reserved for RT (aFRR) service.

    Returns:
        pd.DataFrame: Per-scenario DA_Profit, RT_Profit, and Total_Profit.
    """
    HOURS = scenarios.shape[0]
    capacity_arb = BESS_CAPACITY - capacity_reserved_rt
    P_arb_max = MAX_C_RATE * capacity_arb

    scenario_profits = []

    # Extract scenario indices from column names (fixes undefined-'s' bug)
    scenario_indices = [
        col.split('_s')[1]
        for col in scenarios.columns
        if col.startswith('DA_Price_s')
    ]

    for s_str in scenario_indices:
        s = int(s_str)
        DA_prices = scenarios[f'DA_Price_s{s_str}'].values
        RT_prices = scenarios[f'RT_Price_s{s_str}'].values

        avg_DA_price = DA_prices.mean()
        soc_arb = capacity_arb * 0.5
        total_arb_profit = 0.0

        for hour in range(HOURS):
            price_da = DA_prices[hour]
            price_rt = RT_prices[hour]

            if price_da < avg_DA_price * (1 - DA_ARBITRAGE_THRESHOLD) and soc_arb < capacity_arb:
                charge_power = min(capacity_arb - soc_arb, P_arb_max)
                total_arb_profit -= charge_power * price_rt
                soc_arb += charge_power * 0.95
            elif price_da > avg_DA_price * (1 + DA_ARBITRAGE_THRESHOLD) and soc_arb > 0:
                discharge_power = min(soc_arb, P_arb_max)
                total_arb_profit += discharge_power * 0.95 * price_rt
                soc_arb -= discharge_power

        total_rt_profit = capacity_reserved_rt * RT_AFRR_PRICE * HOURS

        scenario_profits.append({
            'Scenario': s,
            'DA_Profit': total_arb_profit,
            'RT_Profit': total_rt_profit,
            'Total_Profit': total_arb_profit + total_rt_profit,
        })

    return pd.DataFrame(scenario_profits)


def evaluate_expected_profit(scenarios, capacity_reserved_rt):
    """
    Stage-1 objective: expected profit across all equally-weighted scenarios.

    Returns:
        tuple: (expected_profit: float, scenario_results: pd.DataFrame)
    """
    scenario_results = solve_scenario_optimization(scenarios, capacity_reserved_rt)
    num_scenarios = len(scenario_results)
    probability = 1 / num_scenarios
    expected_profit = (scenario_results['Total_Profit'] * probability).sum()
    return expected_profit, scenario_results
