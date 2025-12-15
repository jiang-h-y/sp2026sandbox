import requests
import json
from typing import List

URL = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6ImppYW5nLmhlaUBub3J0aGVhc3Rlcm4uZWR1IiwiZHVlRGF0ZSI6IjIwMjUtMTItMTlUMDU6MDA6MDAuMDAwWiJ9LCJoYXNoIjoiUmhDdUx2SFBub3dYQjZ1M1RCVSJ9"

def get_avg_round_score(has_played: bool, rounds, session_ids):
    if not has_played:
        return "N/A"
    
    scores = []

    for r in rounds:
        if r["sessionId"] in session_ids:
            scores.append(r["score"])
    
    return round(sum(scores) / len(scores), 2)

def get_avg_session_duration(has_played: bool, sessions: List, session_ids: List) -> str | float:
    if not has_played:
        return "N/A"
    
    # create a durations list to keep track of duration times and number of sessions (list length)
    durations = []

    for s in sessions:
        # TODO: what about accidentally duplicated sessions? double counted?
        if s["sessionId"] in session_ids:
            durations.append(s["endTime"] - s["startTime"])
    
    return round(sum(durations) / len(durations), 2)

def get_participant_stats(participant: dict, sessions: List, rounds: List) -> dict:
    id = participant["participantId"]
    # identify if the participant has played any rounds to prevent checking in multiple functions
    has_played = True if len(participant["sessions"]) > 0 else False
    session_ids = participant["sessions"]

    participant_stats = {
        "id": id,
        "name": participant["name"],
        "averageRoundScore": get_avg_round_score(has_played, rounds, session_ids),
        "averageSessionDuration": get_avg_session_duration(has_played, sessions, session_ids)
    }

    return participant_stats

def main():
    with open("sample_data.json", "r") as file:
        data = json.load(file)

    # data = requests.get(URL).json()
    # print(data)
    
    statistics = []
    sessions = data["sessions"]
    rounds = data["rounds"]

    for participant in data["participantInfo"]:
        participant_stats = get_participant_stats(participant, sessions, rounds)
        statistics.append(participant_stats)
    
    print(statistics)

if __name__ == "__main__":
    main()