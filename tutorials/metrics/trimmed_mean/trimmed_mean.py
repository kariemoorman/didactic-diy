import numpy as np
from scipy import stats


def scipy_trimmed_mean(data):
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


def trimmed_mean(data, percentage):
    # Define the trimming proportion
    percentile = int((1 - percentage) * 100)
    trim_proportion = percentage
    # Calculate the number of values to trim
    num_to_trim = int(len(data) * trim_proportion)
    # Sort the data
    sorted_data = np.sort(data)
    # Trim the data by removing values from both ends
    trimmed_data = sorted_data[num_to_trim:-num_to_trim]
    # Calculate the trimmed mean
    trimmedMean = np.mean(trimmed_data)
    print(f"\nTrimmed Mean ({percentile}th Percentile):", trimmedMean)
    # Display the trimmed values
    print("Trimmed Values:")
    print("  Lower End:", sorted_data[:num_to_trim])  # Values removed from the lower end
    print("  Upper End:", sorted_data[-num_to_trim:])  # Values removed from the upper end


# Example
# Create an array of data
#data = np.array([1, 1, 1, 2, 3, 3, 4, 5, 22, 44, 88, 94, 101, 111, 121, 135, 144, 163, 212, 222, 234, 282, 322, 432, 682, 723, 1001])

#scipy_trimmed_mean(data)
#trimmed_mean(data, 0.05)
