import openpyxl
import requests

# Load the Excel file
workbook = openpyxl.load_workbook('23-2073.xlsx')
sheet = workbook.active

# Iterate over rows and columns to read the data
data = []
for row in sheet.iter_rows(min_row=2, values_only=True):
    # Assuming the data is in the first two columns (A and B)
    print(row)
    if row[0] and row[1]:  # Check if both columns have values
        data.append({'column1': row[0], 'column2': row[1]})

print(data)
