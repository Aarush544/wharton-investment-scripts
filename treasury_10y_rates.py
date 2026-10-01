import csv
import numpy as np

TIME_STEP = 1/252


interest_rates = []

with open("DGS10.csv", "r", encoding="UTF-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        try:
            decimal_rate = float(row[1]) / 100
            interest_rates.append(decimal_rate)
        except:
            pass

rates_array = np.array(interest_rates)
rate_today = rates_array[-1]


daily_changes = np.diff(rates_array)
daily_volatility = daily_changes.std()
annual_volatility = daily_volatility * np.sqrt(252)

slope, intercept = np.polyfit(rates_array[:-1], daily_changes, 1)
reversion_speed = -slope * 252
mean = -intercept/slope

rates_matrix = np.zeros((2521, 10000))
rates_matrix[0, :] = rate_today

for day in range(2520):
    current_rates = rates_matrix[day]
    
    random_shocks = np.random.normal(loc=0.0, scale=1.0, size=10000)
    shocks = annual_volatility * np.sqrt(TIME_STEP) * random_shocks
    drifts = reversion_speed * TIME_STEP * (mean - rates_matrix[day])

    changes = drifts + shocks
    rates_matrix[day + 1] = current_rates + changes


final_row = rates_matrix[-1, :]
expected_rate = final_row.mean()

percentiles = np.percentile(final_row, (5, 95))
cvar_95 = np.mean(final_row[final_row >= percentiles[1]])

one_yr_rates = rates_matrix[252, :]
one_yr_var = np.percentile(one_yr_rates, 95)
one_yr_cvar = np.mean(one_yr_rates[one_yr_rates >= one_yr_var])



print(f"Average Interest Rate: {expected_rate}")
print(f"5th Percentile Value: {percentiles[0]}")
print(f"95th Percentile Value: {percentiles[1]}")
print(f"10 year CVaR: {cvar_95}")




