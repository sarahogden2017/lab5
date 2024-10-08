import tabular as tb
import csv

// write data to csv file
with open('data/groub_4_Lab5.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for row in csv_rows:
        writer.writerow(row)
