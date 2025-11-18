# bid-scrape

Scrapes Active Places and counts the number of sites (indoor/outdoor/all) and subtypes (cricket, golf, hockey, etc.) for one local authority.

How to use the program: [Instructions Document](https://docs.google.com/document/d/1krlJj0UqE7m57763JXM3bg2WlOckMSBd/)  
Walkthrough including code: [Walkthrough Document](https://docs.google.com/document/d/1l8BzNyWgjcPFnrZ8UMlxeIPSnJaoq-mA/)

---

## Libraries Used

- **pandas**: For data manipulation and analysis.  
- **os**: To interact with the file system and identify the latest CSV file.

---

## Step-by-Step Functionality

1. **Identify the Latest Active Places CSV File**  
   - The script scans the current directory for CSV files ending with `active_places.csv`.  
   - It selects the most recently modified file as the input dataset.  
   - If no such file is found, the script raises an error.

2. **Extract the Base Name from the File**  
   - The script extracts the portion of the filename before `active_places` to use as a prefix for output files.

3. **Load and Filter Data**  
   - The CSV file is loaded into a pandas DataFrame.  
   - Rows where `Operational Status` is "No Grass Pitches Currently Marked Out" are removed.  
   - Only the following columns are retained:  
     - Site Name  
     - Facility Type  
     - Facility Subtype  
     - Unit  
     - Number  
     - Management Type (Text)

4. **Categorize Facility Type**  
   - A new column `Type/Subtype` is created:  
     - If `Facility Type` is Grass Pitches or Golf, it retains `Facility Subtype`.  
     - Otherwise, it retains `Facility Type`.

5. **Classify Facilities as Indoor or Outdoor**  
   - A predefined list of indoor and outdoor facility types is used.  
   - The script adds a new column `Indoor/Outdoor` based on these lists.

6. **Standardize Units**  
   - The script maps certain unit names to standardized terms in a new column `New Units`.

7. **Adjust Facility Numbers**  
   - Some facility types (e.g., fitness studios, ski slopes, ice rinks) are assigned a default `New Number` of 1.  
   - Otherwise, `New Number` retains its original value.

8. **Standardize Facility Names**  
   - The script applies predefined mappings to create a `New Type/Subtype` column with consistent naming conventions.

---

## Data Summarization and Output Generation

9. **Summarizing Facilities by Category**  
   - The script filters data separately for indoor and outdoor facilities.  
   - It creates summary tables listing each facility type along with:  
     - Number of unique sites  
     - Total count of facilities  
     - Standardized unit type

10. **Unique Site Counts**  
    - The script calculates:  
      - The total number of unique sites  
      - The count of outdoor and indoor sites separately  
      - The count of educational sites for each category

11. **Generate an Excel File**  
    - The processed data is written to an Excel file named `<base_name> Bid Scrape.xlsx`.  
    - The file contains the following sheets:  
      - `Unique site counts`: Summary of unique site statistics  
      - `Outdoor`: Summary of outdoor facility data  
      - `Indoor`: Summary of indoor facility data  
    - Each DataFrame is written without index columns for clarity
