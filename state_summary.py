def get_summary_for_state(state, meeting):
    """
    Returns a tuple summarizing the key parts of the meeting relevant to a state.
    Used to detect changes even if the state remains the same.
    """
    if not meeting:
        return None

    if state == "B":
        return (
            meeting.get("Enter the seminar topic"),
            meeting.get("Enter speaker name here"),
            meeting.get("The DATE when the seminar will be held:"),
            meeting.get("Seminar START time:"),
        )

    elif state == "C":
        return (
            meeting.get("Enter the seminar topic"),
            meeting.get("Enter speaker name here"),
            meeting.get("Please upload a PHOTO of the speaker here:"),
            meeting.get("Abstract of the seminar:"),
        )

    return None
