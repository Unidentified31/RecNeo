import pandas as pd
import os
from scipy.stats import zscore

# File paths
input_file_path = r"C:\Users\*******.csv" # Put the file directory here
output_directory = r"C:\Users\******" # Put the output directory here
output_file_path = os.path.join(output_directory, "******.csv") # Put the output file path here

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Load the data
df = pd.read_csv(input_file_path)

# Calculate Z-scores for Total Fixation
df['Z_Total_Fixation'] = zscore(df['Total_Fixation'])

# Rank Mean Fixation, Variance, and Standard Deviation
df['Ranked_Mean_Fixation'] = df['Mean_Fixation'].rank(ascending=False)
df['Ranked_Variance_Fixation'] = df['Variance_Fixation'].rank(ascending=False)
df['Ranked_Standard_Deviation'] = df['Standard_Deviation'].rank(ascending=False)

# Save the results to a new CSV file
df.to_csv(output_file_path, index=False)

print(f"Results saved to {output_file_path}")
