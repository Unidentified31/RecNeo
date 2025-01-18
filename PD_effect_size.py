import pandas as pd
from scipy.stats import ttest_ind
from math import sqrt

# Load the data from the Excel file
file_path = "****"  # Replace with the correct file path
output_path = "****"  # Output file path
data = pd.read_excel(file_path)

# Ensure column names are trimmed and consistent
data.columns = data.columns.str.strip()

# Check column names
print("Columns in the dataset:", data.columns)

# Separate data based on Role
neologisms = data[data["Role"] == "Neologism"]["PD"]
non_neologisms = data[data["Role"] == "Non-Neologism"]["PD"]

# Calculate mean and standard deviation for each group
mean_neo = neologisms.mean()
std_neo = neologisms.std()
mean_non = non_neologisms.mean()
std_non = non_neologisms.std()

# Calculate pooled standard deviation
n_neo = len(neologisms)
n_non = len(non_neologisms)
pooled_std = sqrt(((n_neo - 1) * std_neo**2 + (n_non - 1) * std_non**2) / (n_neo + n_non - 2))

# Calculate Cohen's d
cohens_d = (mean_neo - mean_non) / pooled_std

# Save results to an Excel file
result = pd.DataFrame({
    "Metric": ["Mean Neologisms", "Mean Non-Neologisms", "Std Neologisms", "Std Non-Neologisms", "Cohen's d"],
    "Value": [mean_neo, mean_non, std_neo, std_non, cohens_d]
})

result.to_excel(output_path, index=False)

print(f"Effect size calculation saved to {output_path}")
