# SAP_Processor
This project processes SAP extracted data for forecasting plant volumes and puts into more readable, smaller formats.

There are two files in the project, one class to prepare file loading and naming (filenamer.py), and the second the code to process the files (converter.py).

The function 'txt_to_csv' of processor.py uses the txt extracted from SAP, removes tabs and creates a more readable csv output.

The function 'from_csv_to_pivot_csv' uses the file generated from txt_to_csv to create a dataframe, sum the requirements per month, delete the original csv created, and finally outputs a pivot csv file and normal tabular file.
