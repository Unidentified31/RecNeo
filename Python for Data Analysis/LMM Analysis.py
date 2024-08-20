import pandas as pd
import statsmodels.formula.api as smf
import os

# Install lxml if not already installed
# try:
   #  import lxml
# except ImportError:
 #    import pip
  #   pip.main(['install', 'lxml'])

# File paths
input_file_path = r"C:\Users\******" # Put the file directory here
output_directory = r"C:\Users\*****" # Put the output directory here
output_file_path = os.path.join(output_directory, "result_Pause_****.txt")  # Save as .txt for readability

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Load the data from the Excel file
df = pd.read_excel(input_file_path)

# Check the structure of the DataFrame
print(df.head())

# Fit a Linear Mixed-Effects Model
model = smf.mixedlm("Fixation_Duration ~ Word", data=df, groups=df["Participant"])
result = model.fit()

# Print the summary of the model
print(result.summary())

# Extract the summary tables as dataframes
summary_html = result.summary().tables[1].to_html()
summary_df = pd.read_html(summary_html, header=0, index_col=0)[0]

# Filter for statistically significant results (p-value < 0.05)
significant_results = summary_df[summary_df['P>|z|'] < 0.05]

# Sort by coefficients
sorted_significant_results = significant_results.sort_values(by='Coef.', ascending=False)

# Interpret the sorted significant results
interpretation = "Interpretation of Significant Results:\n"
for index, row in sorted_significant_results.iterrows():
    interpretation += f"{index}: Coefficient = {row['Coef.']}, " \
                      f"p-value = {row['P>|z|']}\n"

# Save the summary and interpretation to a file
with open(output_file_path, "w") as f:
    f.write(result.summary().as_text())
    f.write("\n\n")
    f.write(interpretation)

print(f"Results saved to {output_file_path}")

# Output significant results and interpretation to console
print("\nSignificant Results:")
print(sorted_significant_results)
print("\nInterpretation of Significant Results:")
print(interpretation)
