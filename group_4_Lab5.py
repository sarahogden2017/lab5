import tabula as tb
import PyPDF2 as pypdf
from itertools import chain
import re
import csv

# Name of the PDF file we're working with
filename = "data/Table9.pdf"
data_pages = []
table = []

headers = None

# Open the PDF file and read its contents
with open(filename, "rb") as pdfFile:
    reader = pypdf.PdfReader(pdfFile)

    # Extract text from each page of the PDF
    for page in reader.pages:
        data_pages.append(page.extract_text())

# Process each page of extracted data
for p in range(len(data_pages)):
    # Split the page text to separate the table data from the column titles
    split_page = data_pages[p].split("TABLE 9")
    # Remove any empty items at the beginning
    split_page.pop(0)

    # Split the table data into rows
    table_data = split_page[0].split('\n')

    # Remove the first empty item
    table_data.pop(0)

    # Find rows that are incomplete (split across pages)
    # We do this by checking the number of spaces in each row
    short_row = []
    for i in range(len(table_data)):
        if table_data[i].count(' ') < 14:
            short_row.append(i)

    # Fix incomplete rows by merging them with the next row
    for i in short_row:
        table_data[i: i + 2] = [''.join(table_data[i: i + 2])]

    # Split each row into individual items and clean up the data
    for i in range(len(table_data)):
        table_data[i] = table_data[i].split(' ')
        # Remove empty values and dashes
        table_data[i] = [e for e in table_data[i] if e and e != '–']
        for e in range(len(table_data[i])):
            if table_data[i][e].isdigit() is True:
                # This is a number, we could process it further if needed
                pass
            else:
                # This is not a number, we might want to handle it differently
                pass

    # Save the column headers from the first page
    if p == 0:
        headers = split_page[1]

    # Add the processed data from this page to our main table
    table.append(table_data)

# Flatten our list of lists into a single list
table = list(chain(*table))

# Remove the summary indicator table at the end of the main table

# Find where the summary table begins
index = table.index([])
# Remove everything after that index
table = table[:index]

# Clean up the data: remove non-numeric elements from the end of each row
for row in table:
    for e in reversed(range(len(row))):
        if e > 0:
            element = row[e]
            if element != '–' and element.isdigit() == False:
                row.pop(e)

# Clean up the headers
headers = headers.replace("78      THE STATE OF THE WORLD'S CHILDREN 2014 IN NUMBERS", "")
headers = headers.replace("    CHILD PROTECTION", "")

# Split headers based on capital letters
headers = re.split('(?<=.)(?=[A-Z])', headers)

# Clean up the first 7 headers
for r in range(len(headers)):
    if r < 7:
        headers[r] = headers[r].replace("\n", " ")

# Process the bottom headers
bottom_headers = headers[6][len("Violent discipline (%)+   2005–2012*"):]
headers[6] = headers[6][:len("Violent discipline (%)+  2005–2012*")]

bottom_headers_list = [bottom_headers[:len("prevalence attitudes total male female")]]
bottom_headers_list.append(bottom_headers[len("prevalence attitudes total male female"):])

headers_married_NM = bottom_headers.replace("prevalence attitudes total male female ", "")
bottom_headers = bottom_headers_list[0].split()
bottom_headers.append(headers_married_NM[:len("married by 15")])

headers_married_NM = headers_married_NM.replace("married by 15 ", "")
bottom_headers.append(headers_married_NM[:len("married by 18")])

headers_married_NM = headers_married_NM.replace("married by 18 ", "")
bottom_headers.append(headers_married_NM[:len("women")])

headers_married_NM = headers_married_NM.replace("womena", "")
bottom_headers.append(headers_married_NM[:len("girls")])

headers_married_NM = headers_married_NM.replace("girlsb", "")
bottom_headers.append(headers_married_NM[:len("support for the  practice")])

# Prepare the final list of headers
all_headers = []

# Remove everything after '(' in each header
headers = [header.split(" (")[0] for header in headers]

# Add the first header (country name)
all_headers.append(headers[0])

# Define combinations of main headers and sub-headers
combinations = [
    # Child labour headers
    (headers[1], bottom_headers[2]), (headers[1], bottom_headers[3]), (headers[1], bottom_headers[4]),
    # Child marriage headers
    ("Child", bottom_headers[5]), ("Child", bottom_headers[6]),
    # Birth registration headers
    (headers[4], bottom_headers[0]), (headers[4], bottom_headers[7]), (headers[4], bottom_headers[8]),
    # Justification of wife beating headers
    (headers[5], bottom_headers[3]), (headers[5], bottom_headers[4]),
    # Violent discipline headers
    (headers[6], bottom_headers[2]), (headers[6], bottom_headers[3]), (headers[6], bottom_headers[4])
]

# Combine headers
for combo in combinations:
    if combo[0] == "Child":
        all_headers.append("Child_" + combo[1])
    else:
        all_headers.append(combo[0] + "_" + combo[1])

# Replace spaces with underscores in all headers
all_headers = [header.replace(" ", "_") for header in all_headers]

# Add the final header (FGM/C prevalence)
all_headers.append(headers[3])

# Prepare the data for CSV output
answer_list = [["CountryName", "CategoryName", "CategoryTotal"]]
for row in table:
    for e in range(len(row)):
        temp_list = [row[0], all_headers[e]]
        if e > 0 and row[e] != '–' and row[e].isdigit() is True:
            temp_list.append(row[e])
            answer_list.append(temp_list)

# Write the processed data to a CSV file
with open('group_4_lab5.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(answer_list)

# Print the total number of data rows in the CSV file
print(f"The total number of rows in the csv file is {len(answer_list) - 1}")

