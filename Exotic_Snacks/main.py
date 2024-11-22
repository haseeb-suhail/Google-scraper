import csv

# Open the original CSV file and the new CSV file for filtered results
with open('Exotic_Snacks_Data.csv', 'r', encoding='utf-8') as infile, open('filtered_google_search_exotics.csv', 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write the header to the new CSV file including additional fields
    headers = next(reader)
    writer.writerow(headers + ['Links'])

    # Filter and write the rows containing "exoticsnack" or "exoticsnacks" to the new file
    for row in reader:
        keyword = row[0]
        company_name = row[1]
        full_address = row[2]
        category = row[3]
        phone_no = row[4]
        link = row[5]
        google_map_url = row[6]

        if 'exoticsnack' in link.lower() or 'exoticsnacks' in link.lower():
            writer.writerow([keyword, company_name, full_address, category, phone_no, link, google_map_url])

print("Filtered links have been saved to filtered_google_search_exotics.csv")
