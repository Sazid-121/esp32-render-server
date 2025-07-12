import gspread
from datetime import datetime
import pytz

# Constants (you can move to config.py later if needed)
SERVICE_ACCOUNT_FILE = "service_account.json"
GOOGLE_SHEET_ID = "1w9C-oExk3cBsDNirHMABl1aJhoZZaNff6hUUJCnnUKw"
WORKSHEET_NAME = "Form Responses 1"

# Initialize timezone
dhaka_tz = pytz.timezone("Asia/Dhaka")

# Field mapping based on actual column titles
FIELD_MAP = {
    "date": "Choose the DATE when the seminar will be held:",
    "start_time": "Seminar START time:",
    "end_time": "Seminar END time:",
}


def load_worksheet():
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    sh = gc.open_by_key(GOOGLE_SHEET_ID)
    return sh.worksheet(WORKSHEET_NAME)


def fetch_latest_valid_meetings():
    worksheet = load_worksheet()
    rows = worksheet.get_all_records()

    now = datetime.now(dhaka_tz)
    valid_entries = []
    rows_to_delete = []

    for idx, row in enumerate(rows):
        try:
            date_str = row[FIELD_MAP["date"]].strip()
            start_time_str = row[FIELD_MAP["start_time"]].strip()
            end_time_str = row[FIELD_MAP["end_time"]].strip()

            # Parse datetime with seconds and AM/PM
            start_dt = dhaka_tz.localize(datetime.strptime(f"{date_str} {start_time_str}", "%m/%d/%Y %I:%M:%S %p"))
            end_dt = dhaka_tz.localize(datetime.strptime(f"{date_str} {end_time_str}", "%m/%d/%Y %I:%M:%S %p"))

            # Skip and mark past meetings for deletion
            if now >= end_dt:
                rows_to_delete.append(idx + 2)  # account for header + 1-based indexing
                continue

            row['__start_dt'] = start_dt
            row['__end_dt'] = end_dt
            valid_entries.append(row)

        except Exception as e:
            print(f"[Warning] Row {idx+2} skipped due to parsing error: {e}")

    for row_idx in reversed(rows_to_delete):
        worksheet.delete_rows(row_idx)
        print(f"[Info] Deleted past event row {row_idx}")

    return valid_entries
