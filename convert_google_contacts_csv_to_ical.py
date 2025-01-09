import pandas as pd
from datetime import datetime

def generate_ical_from_csv(csv_file, ical_file):
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Filter necessary columns
    required_columns = ['First Name', 'Middle Name', 'Last Name', 'Birthday']
    df = df[required_columns]

    # Open the iCal file for writing
    with open(ical_file, 'w', encoding='utf-8') as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\n")
        f.write("CALSCALE:GREGORIAN\n")

        # Process each row to create an iCal entry
        for _, row in df.iterrows():
            first_name = row['First Name'] if pd.notna(row['First Name']) else ""
            middle_name = row['Middle Name'] if pd.notna(row['Middle Name']) else ""
            last_name = row['Last Name'] if pd.notna(row['Last Name']) else ""
            birthday = row['Birthday']

            # Skip rows without a valid birthday
            if pd.isna(birthday):
                continue

            birthday = birthday.strip()
            # Handle birthday format
            if birthday.startswith('--'):  # Format: --MM-DD
                birthday_date = datetime.strptime(birthday, "--%m-%d")
            else:  # Format: YYYY-MM-DD
                birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
            start_date = birthday_date.strftime("%Y%m%d")

            # Create the calendar entry
            if middle_name == "":
                summary = f"{first_name} {last_name} Geburtstag".strip()
            else:
                summary = f"{first_name} {middle_name} {last_name} Geburtstag".strip()
            uid = f"{first_name.lower()}-{last_name.lower()}-{start_date}@example.com".replace(" ", "")

            f.write("BEGIN:VEVENT\n")
            f.write(f"SUMMARY:{summary}\n")
            f.write(f"DTSTART;VALUE=DATE:{start_date}\n")
            f.write(f"RRULE:FREQ=YEARLY\n")
            f.write(f"UID:{uid}\n")
            f.write("STATUS:CONFIRMED\n")
            f.write("SEQUENCE:0\n")
            f.write("TRANSP:TRANSPARENT\n")
            f.write("END:VEVENT\n")

        f.write("END:VCALENDAR\n")

# Usage
csv_file_path = r'<<INSERT_CSV_FILE_PATH>>'
ical_file_path = r'<<INSERT_ICAL_FILE_PATH>>'
generate_ical_from_csv(csv_file_path, ical_file_path)
