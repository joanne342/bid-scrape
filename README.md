How to use the program: https://docs.google.com/document/d/1krlJj0UqE7m57763JXM3bg2WlOckMSBd/

Walkthrough including code: https://docs.google.com/document/d/1l8BzNyWgjcPFnrZ8UMlxeIPSnJaoq-mA/

*Libraries Used*<br>
    • pandas: For data manipulation and analysis.<br>
    • os: To interact with the file system and identify the latest CSV file.

*Step-by-Step Functionality*

1. Identify the Latest Active Places CSV File<br>
    • The script scans the current directory for CSV files ending with active_places.csv.<br>
    • It selects the most recently modified file as the input dataset.<br>
    • If no such file is found, the script raises an error.

2. Extract the Base Name from the File<br>
    • The script extracts the portion of the filename before active_places to use as a prefix for output files.

3. Load and Filter Data<br>
    • The CSV file is loaded into a pandas DataFrame.<br>
    • Rows where Operational Status is "No Grass Pitches Currently Marked Out" are removed.<br>
    • Only the following columns are retained:<br>
        o Site Name<br>
        o Facility Type<br>
        o Facility Subtype<br>
        o Unit<br>
        o Number<br>
        o Management Type (Text)

4. Categorize Facility Type<br>
    • A new column Type/Subtype is created:<br>
        o If Facility Type is Grass Pitches or Golf, it retains Facility Subtype.<br>
        o Otherwise, it retains Facility Type.

5. Classify Facilities as Indoor or Outdoor<br>
    • A predefined list of indoor and outdoor facility types is used.<br>
    • The script adds a new column Indoor/Outdoor based on these lists.

6. Standardize Units<br>
    • The script maps certain unit names to standardized terms in a new column New Units.

7. Adjust Facility Numbers<br>
    • Some facility types (e.g., fitness studios, ski slopes, ice rinks) are assigned a default New Number of 1.<br>
    • Otherwise, New Number retains its original value

8. Standardize Facility Names<br>
    • The script applies predefined mappings to create a New Type/Subtype column with consistent naming conventions.

*Data Summarization and Output Generation*

9. Summarizing Facilities by Category<br>
    • The script filters data separately for indoor and outdoor facilities.<br>
    • It creates summary tables listing each facility type along with:<br>
        o Number of unique sites<br>
        o Total count of facilities<br>
        o Standardized unit type

10. Unique Site Counts<br>
    • The script calculates:<br>
        o The total number of unique sites.<br>
        o The count of outdoor and indoor sites separately.<br>
        o The count of educational sites for each category.

11. Generate an Excel File<br>
    • The processed data is written to an Excel file named <base_name> Bid Scrape.xlsx.<br>
    • The file contains the following sheets:<br>
        o Unique site counts: Summary of unique site statistics.<br>
        o Outdoor: Summary of outdoor facility data.<br>
        o Indoor: Summary of indoor facility data.<br>
    • Each DataFrame is written without index columns for clarity.



