import pandas as pd
import os

# Find the newest CSV file that ends with 'active_places.csv' in the same directory as the script
current_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script
csv_file = None

# Initialize variables to track the newest file
latest_file = None
latest_mod_time = 0

# Search for the newest file ending with 'active_places.csv'
for file in os.listdir(current_dir):
    if file.endswith('active_places.csv'):
        file_path = os.path.join(current_dir, file)
        mod_time = os.path.getmtime(file_path)  # Get the file's modification time
        if mod_time > latest_mod_time:
            latest_mod_time = mod_time
            latest_file = file_path

# Check if a file was found
if latest_file is None:
    raise FileNotFoundError("No file ending with 'active_places.csv' found in the current directory.")

# Use the newest file as the CSV file
csv_file = latest_file

# Extract the part of the file name before " active_places"
file_base_name = os.path.basename(csv_file).split(" active_places")[0]

# Load the CSV file
df = pd.read_csv(csv_file)

# Filter out rows where "Operational Status" is "No Grass Pitches Currently Marked Out"
df = df[df['Operational Status'] != "No Grass Pitches Currently Marked Out"]

# Retain only the desired columns
columns_to_keep = ['Site Name', 'Facility Type', 'Facility Subtype', 'Unit', 'Number', 'Management Type (Text)']
df = df[columns_to_keep]

# Add a new column 'Type/Subtype' based on the conditions
df['Type/Subtype'] = df.apply(
    lambda row: row['Facility Subtype'] if row['Facility Type'] in ['Grass Pitches', 'Golf'] else row['Facility Type'],
    axis=1
)

# Define Indoor and Outdoor categories
indoor_facilities = [
    "Health and Fitness Gym",
    "Indoor Bowls",
    "Indoor Tennis Centre",
    "Sports Hall",
    "Squash Courts",
    "Studio",
    "Swimming Pool",
    'Ice Rinks',
    'Ski Slopes'
]

outdoor_facilities = [
    "Artificial Grass Pitch",
    "Athletics",
    "Grass Pitches",
    "Outdoor Tennis Courts",
    "Golf",
    "Bowling Green",
    'Cycling'
]

# Add a new column 'Indoor/Outdoor'
df['Indoor/Outdoor'] = df['Facility Type'].apply(
    lambda x: "Indoor" if x in indoor_facilities else 
              "Outdoor" if x in outdoor_facilities else 
              None
)

# Define mapping for the 'Unit' to 'New Units' transformation
unit_mapping = {
    "Badminton Courts": "Courts",
    "Bike Stations": "Studios",
    "Partitionable Spaces": "Studios",
    "n/a": "Lanes",
    "Oval Track Lanes": "Lanes",
    "Straight Track Lanes": "Lanes"
}

# Add a new column 'New Units'
df['New Units'] = df.apply(
    lambda row: row['Facility Type'] if pd.isna(row['Unit']) else unit_mapping.get(row['Unit'], row['Unit']),
    axis=1
)

# Add a new column 'New Number'
df['New Number'] = df.apply(
    lambda row: 1 if row['Facility Subtype'] in ['Fitness Studio', 'Cycle Studio'] or row['Facility Type'] in ['Ski Slopes', 'Cycling', 'Ice Rinks'] else row['Number'],
    axis=1
)

# Add a new column 'New Type/Subtype' based on the transformation rules
type_subtype_mapping = {
    "Health and Fitness Gym": "Health and Fitness",
    "Indoor Tennis Centre": "Indoor Tennis",
    "Sports Hall": "Sports Halls",
    "Athletics": "Athletics Track",
    "Driving Range": "Golf - Driving Range",
    "Par 3": "Golf - Par 3",
    "Standard": "Golf - Standard",
    "Outdoor Tennis Courts": "Tennis Courts"
}

df['New Type/Subtype'] = df['Type/Subtype'].apply(
    lambda x: type_subtype_mapping.get(x, x)  # Use the mapping if found, otherwise keep original
)

#================================================================================================
# Indoor/outdoor section

# Filter the df for each category and create DataFrames
indoor_df = df[df['Indoor/Outdoor'] == 'Indoor']
outdoor_df = df[df['Indoor/Outdoor'] == 'Outdoor']

# Function to process each category into a DataFrame
def process_data(df):
    # Get the unique values from 'New Type/Subtype' and sort them alphabetically
    all_types = df.sort_values(['Indoor/Outdoor', 'New Type/Subtype'])['New Type/Subtype'].unique()

    # Convert the list of 'New Type/Subtype' values into a DataFrame
    all_types_df = pd.DataFrame(all_types, columns=['Facility'])

    # Add new blank columns
    all_types_df['Sites'] = ''
    all_types_df['Unit'] = ''
    all_types_df['Number'] = ''

    # Create a deduplicated dictionary mapping 'New Type/Subtype' to 'New Units'
    deduped_dict = pd.Series(df['New Units'].values, index=df['New Type/Subtype']).to_dict()

    # Map the 'Facility' values in all_types_df to 'Unit' using deduped_dict
    all_types_df['Unit'] = all_types_df['Facility'].map(deduped_dict)

    # Group by 'New Type/Subtype' and sum the 'New Number' values
    summed_numbers = df.groupby('New Type/Subtype')['New Number'].sum()

    # Map the summed values to 'Number' in all_types_df based on 'Facility'
    all_types_df['Number'] = all_types_df['Facility'].map(summed_numbers)

    # Group df by 'New Type/Subtype' and count unique 'Site Name' entries
    unique_sites_count = df.groupby('New Type/Subtype')['Site Name'].nunique()

    # Map the unique site counts to the 'Sites' column in all_types_df based on 'Facility'
    all_types_df['Sites'] = all_types_df['Facility'].map(unique_sites_count)

    return all_types_df

# Process data for each category
indoor_data = process_data(indoor_df)
outdoor_data = process_data(outdoor_df)

# Modify the unique_sites_data section to include the "Educational Sites" column
unique_sites_data = {
    'Unique sites across categories': ['All', 'Outdoor', 'Indoor'],
    'Number': [
        # Count for All sites
        df['Site Name'].nunique(),
        
        # Count for Outdoor sites
        df[df['Indoor/Outdoor'] == 'Outdoor']['Site Name'].nunique(),
        
        # Count for Indoor sites
        df[df['Indoor/Outdoor'] == 'Indoor']['Site Name'].nunique(),
    ],
    'Educational Sites': [
        # Educational sites count (same as "All Educational" sites for each category)
        df[df['Management Type (Text)'].str.contains('School/College/University (in house)', case=False, na=False, regex=False)]['Site Name'].nunique(),
        
        # Count for Outdoor Educational sites
        df[(df['Indoor/Outdoor'] == 'Outdoor') & df['Management Type (Text)'].str.contains('School/College/University (in house)', case=False, na=False, regex=False)]['Site Name'].nunique(),
        
        # Count for Indoor Educational sites
        df[(df['Indoor/Outdoor'] == 'Indoor') & df['Management Type (Text)'].str.contains('School/College/University (in house)', case=False, na=False, regex=False)]['Site Name'].nunique()
    ]
}

# Create a DataFrame from the modified unique_sites_data
unique_sites_df = pd.DataFrame(unique_sites_data)

# Create the output file name by prepending the base file name
output_filename = f"{file_base_name} Bid Scrape.xlsx"

# Write all DataFrames to an Excel file with separate sheets
with pd.ExcelWriter(output_filename) as writer:
    unique_sites_df.to_excel(writer, sheet_name='Unique site counts', index=False)
    outdoor_data.to_excel(writer, sheet_name='Outdoor', index=False)
    indoor_data.to_excel(writer, sheet_name='Indoor', index=False)

print(f"Excel file '{output_filename}' saved successfully.")

