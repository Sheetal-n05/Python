# a Python script that will import the virus_results.csv file and work with that data. The raw data file is made up of 5 columns:

# VirusName - the name of the virus being tested for
# CalendarMonth - the month in which the testing occurred
# CalendarYear - the year in which the testing occurred
# PositiveCount - the number of positive results for that virus and calendar month
# NegativeCount - the number of negative results for that virus and calendar month


# Program - Create a table with 1 row per virus, displaying the calendar month with the highest positivity (positives / total tested).  The table should look similar to this:

# Import libraries
import csv
import os
import datetime

# Provide input and output filepath
filename = os.path.join("virus_results.csv")
analysis = os.path.join("table_2.txt")

# Initialize dictionaries
high_positivity_monthly = {}
virus_data_yearly = {}
yearly_totals = {}

# Read the virus result data in dictionary
with open(filename) as csv_file:
    reader = csv.DictReader(csv_file)

    # loop over the the file and save columnname in variable
    for row in reader:
        virus_name = row['VirusName'].rstrip()
        calender_month = row["CalendarMonth"].split('/')
        calendar_year = row['CalendarYear']
        positive_count = int(row['PositiveCount'])  # 204
        negative_count = int(row['NegativeCount'])  # 4452

        # Calculate total tests and positivity
        total_test = positive_count + negative_count  # 4656
        positivity = (positive_count / total_test) * 100 if total_test > 0 else 0

        # MONTHLY POSITIVITY ANALYSIS ACROSS ALL VIRUSES
        month_number, _, year_full_number = calender_month
        month_name = datetime.datetime.strptime(month_number, "%m").strftime("%b")
        year_formatted = year_full_number[-2:]
        month_year = f"{month_name}-{year_formatted}"

        # check if dictionary has highest postivity
        if virus_name not in high_positivity_monthly or high_positivity_monthly[virus_name]['positivity'] < positivity:
            high_positivity_monthly[virus_name] = {
                'month': month_year,
                'positivity': round(positivity, 1)}

        # YEARLY ANALYSIS ACROSS ALL VIRUSES  FOR ALL YEARS
        if virus_name not in virus_data_yearly:
            virus_data_yearly[virus_name] = {}
        if calendar_year not in virus_data_yearly[virus_name]:
            virus_data_yearly[virus_name][calendar_year] = {'positive': 0, 'negative': 0}

        # update dictionary incrementing postive and negative count
        virus_data_yearly[virus_name][calendar_year]['positive'] += positive_count
        virus_data_yearly[virus_name][calendar_year]['negative'] += negative_count

        # Aggregate counts per year
        if calendar_year not in yearly_totals:
            yearly_totals[calendar_year] = {'positive': 0, 'negative': 0}
        yearly_totals[calendar_year]['positive'] += positive_count
        yearly_totals[calendar_year]['negative'] += negative_count

# HIGHEST AND LOWEST POSITIVITY ACROSS ALL VIRUSES AND YEARES
highest_positivity_yearly = {}

# Loop over each virus and its corresponding yearly data in the virus_data_yearly dictionary
for virus, virus_years_counts in virus_data_yearly.items():
    best_year = None
    highest_rate = 0.0
    for year, pos_neg_counts in virus_years_counts.items():
        total = pos_neg_counts['positive'] + pos_neg_counts['negative']
        if total > 0:
            rate = pos_neg_counts['positive'] / total
            if rate > highest_rate:
                highest_rate = rate
                best_year = year
    # store the best year and highest rate for virus in the dictionary
    highest_positivity_yearly[virus] = [best_year, highest_rate]

# Initialize year and rate
highest_year = None
lowest_year = None
highest_rate = 0.0
lowest_rate = 1.0

# Loop through dictionart and get the count for total test
for year, pos_neg_count in yearly_totals.items():
    total_tests = pos_neg_count['positive'] + pos_neg_count['negative']
    if total_tests > 0:
        rate = pos_neg_count['positive'] / total_tests
        # Calculate overall positivity rates and years with highest and lowest rates
        if rate > highest_rate:
            highest_rate = rate
            highest_year = year
        if rate < lowest_rate:
            lowest_rate = rate
            lowest_year = year

# save monthly result
result_month = ('\n'.join([f"{'Virus':^18} {'Month':^8} {'Positivity':>8}"] +
                          [f"{virus:<18} {data['month']:^8} {data['positivity']:>8}%"
                           for virus, data in high_positivity_monthly.items()]))

# save yearly result
result_year = ('\n'.join([f"{'Virus':^18} {'Year':^8} {'Positivity':>8}"] +
                         [f"{virus:<18} {year:^8} {rate * 100:>8.1f}%"
                          for virus, [year, rate] in highest_positivity_yearly.items()]))

# save overall result with highest and lowest positivity
result_overall = (
    f"{'Across All Viruses':^20} {'Year':^8} {'Positivity':>8}\n"
    f"{'Highest Positivity':<20} {highest_year:^10} {highest_rate * 100:>8.1f}%\n"
    f"{'Lowest Positivity':<20} {lowest_year:^10} {lowest_rate * 100:>8.1f}%")

# write all the results in text output file
with open(analysis, "w") as file:
    file.write(result_year)

# print results on terminal
print(result_month, '\n\n', result_year, '\n\n', result_overall)

