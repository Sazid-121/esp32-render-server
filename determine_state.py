from datetime import datetime, timedelta
import pytz

dhaka_tz = pytz.timezone("Asia/Dhaka")

def determine_state(valid_meetings):
    """
    Determine current state (A, B, or C) and return:
    - state: "A", "B", or "C"
    - selected_meeting: dict of meeting info (or None if state A)
    """

    now = datetime.now(dhaka_tz)
    if not valid_meetings:
        return "A", None

    # Sort by start time (just in case multiple future meetings exist)
    valid_meetings.sort(key=lambda row: row['__start_dt'])

    for row in valid_meetings:
        start_dt = row['__start_dt']
        end_dt = row['__end_dt']

        state_b_window = start_dt - timedelta(minutes=2)
        state_c_end = end_dt - timedelta(minutes=2)

        if now < state_b_window:
            return "B", row  # Upcoming
        elif state_b_window <= now < state_c_end:
            return "C", row  # Ongoing

    return "A", None  # All meetings are in the past or too close to end
