import numpy as np
from scipy import stats

# Create an array of data
data = np.array([1, 1, 1, 2, 3, 3, 4, 5, 22, 44, 88, 94, 101, 111, 121, 135, 144, 163, 212, 222, 234, 282, 322, 432, 682, 723, 1000, 1001])

# Calculate the trimmed mean values
trimmed_mean_99 = round(stats.trim_mean(data, proportiontocut=0.01), 2)
trimmed_mean_95 = round(stats.trim_mean(data, proportiontocut=0.05), 2)
trimmed_mean_90 = round(stats.trim_mean(data, proportiontocut=0.1), 2)

mean_data = round(np.mean(data), 2)
median_data = round(np.median(data), 2)

print("Median:", median_data)
print("Mean:", mean_data)
print("90% Trimmed Mean:", trimmed_mean_90)
print("95% Trimmed Mean:", trimmed_mean_95)
print("99% Trimmed Mean:", trimmed_mean_99)


## Output 
# Median: 116.0
# Mean: 219.75
# 90% Trimmed Mean: 172.92
# 95% Trimmed Mean: 198.12
# 99% Trimmed Mean: 219.75