import pandas as pd
import statsmodels.formula.api as smf

# Load the data from an Excel file
file_path = "******.xlsx"  # Replace with your actual file path
output_path = "*****.xlsx"  # Output file for results
data = pd.read_excel(file_path)

# Ensure 'Role' and 'Participant' columns are appropriately formatted
data["Role"] = pd.Categorical(data["Role"], categories=["Non-Neologism", "Neologism"], ordered=True)
data["Participant"] = data["Participant"].astype(str)

# Fit a simplified Linear Mixed-Effects Model (LMM) for FD
model = smf.mixedlm(
    formula="PD ~ Role",  # Fixed effect: Role
    data=data,
    groups=data["Participant"],  # Random effect: Participant
    re_formula="~1"  # Random intercept for each participant
)
result = model.fit()

# Print the summary of the model
print(result.summary())

# Extract simplified results into a table
summary_table = pd.DataFrame({
    "Parameter": result.params.index,
    "Estimate": result.params.values,
    "Standard Error": result.bse.values,
    "z-value": result.tvalues,
    "p-value": result.pvalues,
    "Confidence Interval Lower": result.conf_int().iloc[:, 0],
    "Confidence Interval Upper": result.conf_int().iloc[:, 1]
}).query("Parameter in ['Intercept', 'Role[T.Neologism]']")  # Filter only desired parameters

# Add Group Var (Participant Var)
group_var = result.cov_re.iloc[0, 0]  # Extract the variance of the random effect
group_var_row = pd.DataFrame([{
    "Parameter": "Group Var",
    "Estimate": group_var,
    "Standard Error": None,
    "z-value": None,
    "p-value": None,
    "Confidence Interval Lower": None,
    "Confidence Interval Upper": None
}])

# Ensure consistent columns before concatenation
group_var_row = group_var_row[summary_table.columns]  # Align columns
summary_table = pd.concat([summary_table, group_var_row], ignore_index=True)

# Save the table to an Excel file
with pd.ExcelWriter(output_path) as writer:
    summary_table.to_excel(writer, sheet_name="LMM Results", index=False)

print(f"Simplified LMM results saved to {output_path}.")
