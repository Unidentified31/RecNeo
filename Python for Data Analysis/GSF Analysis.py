import pandas as pd
import os

# Load the CSV file
file_path = r"C:\Users\*****.csv"  # Update this to the path of your CSV file
data = pd.read_csv(file_path)

# Initialize the output dictionary
output = {}

# Assuming 'AOI' is the column name where the AOI values are stored
# Check if the column exists to avoid errors
if 'AOI' in data.columns:
    # Count FPOGD with an AOI value (not null or NaN)
    count_with_aoi = data['AOI'].notna().sum()

    # Count total number of FPOGD
    total_count = len(data)

    # Store results in the output dictionary
    output["Number of FPOGD with an AOI value"] = count_with_aoi
    output["Total number of FPOGD"] = total_count

    # Print the results
    print("Number of FPOGD with an AOI value:", count_with_aoi)
    print("Total number of FPOGD:", total_count)
else:
    error_message = "AOI column not found in the data. Please check the column name and try again."
    output["Error"] = error_message
    print(error_message)

# Ensure the directory for the output file exists
output_directory = r"C:\Users\****"  # Update this to your desired output directory
output_file_path = os.path.join(output_directory, "output_results.csv") 

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Convert the output dictionary to a DataFrame and save it to a CSV file
output_df = pd.DataFrame([output])
output_df.to_csv(output_file_path, index=False)
print(f"Results have been saved to {output_file_path}")
