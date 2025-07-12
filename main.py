import time
from datetime import datetime
import pytz
import os

from fetch_sheet import fetch_latest_valid_meetings
from determine_state import determine_state
from render_state_a import render_state_a
from render_state_b import render_state_b
from render_state_c import render_state_c
from convert_to_bin import save_image_as_bin
from version_manager import write_version
from state_summary import get_summary_for_state

# === Initial Setup ===
version = 0
previous_state = None
previous_data = {}

dhaka_tz = pytz.timezone("Asia/Dhaka")

# Output folder for Flask static files
STATIC_DIR = "static"
BIN_PATH = os.path.join(STATIC_DIR, "display_image_rgb565.bin")
VERSION_PATH = os.path.join(STATIC_DIR, "version.txt")

# === Main Loop ===
while True:
    now = datetime.now(dhaka_tz)
    if now.second % 10 == 0:
        print(f"\n[INFO] Checking at {now.strftime('%Y-%m-%d %H:%M:%S')}")

        valid_meetings = fetch_latest_valid_meetings()
        current_state, meeting = determine_state(valid_meetings)

        current_summary = get_summary_for_state(current_state, meeting)
        previous_summary = previous_data.get("summary")

        if current_state != previous_state or current_summary != previous_summary:
            print(f"[INFO] State change or content update: {previous_state} → {current_state}")

            # Increment version
            version = (version + 1) % 10
            write_version(version, VERSION_PATH)

            # === Render according to state ===
            if current_state == "A":
                img = render_state_a()

            elif current_state == "B":
                topic = meeting.get("Enter the seminar topic:", "Unknown Topic")
                speaker = meeting.get("Enter speaker name here:", "Unknown Speaker")
                date = meeting.get("Choose the DATE when the seminar will be held:", "")
                time_ = meeting.get("Seminar START time:", "")
                datetime_str = f"{date}, {time_}"
                img = render_state_b(topic, datetime_str, speaker)

            elif current_state == "C":
                topic = meeting.get("Enter the seminar topic:", "Unknown Topic")
                speaker = meeting.get("Enter speaker name here:", "Unknown Speaker")
                image_url = meeting.get("Please upload a PHOTO of the speaker here:", "")
                abstract = meeting.get("Enter the abstract of the seminar: (in 150 words)", "No abstract provided")
                img = render_state_c(topic, speaker, image_url, abstract)

            else:
                print("[ERROR] Unknown state. Skipping.")
                continue

            # === Save outputs to /static
            save_image_as_bin(img, BIN_PATH)
            print(f"[INFO] Saved new display image → {BIN_PATH}")

            previous_state = current_state
            previous_data["summary"] = current_summary

        else:
            print(f"[INFO] No update needed. Still in state {current_state}.")

        time.sleep(1)

    else:
        time.sleep(0.2)
