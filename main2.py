import requests
import json
from collections import defaultdict

URL = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6ImppYW5nLmhlaUBub3J0aGVhc3Rlcm4uZWR1IiwiZHVlRGF0ZSI6IjIwMjUtMTItMTlUMDU6MDA6MDAuMDAwWiJ9LCJoYXNoIjoiUmhDdUx2SFBub3dYQjZ1M1RCVSJ9"

def process_rounds(rounds):
    """ Aggregates rounds data by session """
    rounds_data = defaultdict(lambda: defaultdict(float))

    for r in rounds:
        session = rounds_data[r["sessionId"]]
        session["score_sum"] += r["score"]
        session["duration_sum"] += r["endTime"] - r["startTime"]
        session["count"] += 1

    return rounds_data

def process_sessions(sessions, rounds_data):
    """ Aggregates sessions data by participant """
    sessions_data = defaultdict(lambda: defaultdict(float))
    languages = defaultdict(lambda: defaultdict(float))

    for s in sessions:
        participant = sessions_data[s["participantId"]]
        participant["round_score_sum"] += rounds_data[s["sessionId"]]["score_sum"]
        participant["session_duration_sum"] += s["endTime"] - s["startTime"]
        participant["session_count"] += 1
        participant["round_count"] += rounds_data[s["sessionId"]]["count"]

        participant_language = languages[(s["participantId"], s["language"])]
        participant_language["round_score_sum"] += rounds_data[s["sessionId"]]["score_sum"]
        participant_language["round_duration_sum"] += rounds_data[s["sessionId"]]["duration_sum"]
        participant_language["round_count"] += rounds_data[s["sessionId"]]["count"]

    return sessions_data, languages

def aggregate_by_participant(participants, sessions_data):
    participants_data = []

    for p in participants:
        individual = {}
        id = p["participantId"]
        individual["id"] = id
        individual["name"] = p["name"]

        individual["languages"] = []

        if len(p["sessions"]) == 0:
            individual["averageRoundScore"] = "N/A"
            individual["averageSessionDuration"] = "N/A"
        else:
            languages_data = {}
            individual["averageRoundScore"] = sessions_data[id]["round_score_sum"] / sessions_data[id]["round_count"]
            individual["averageSessionDuration"] = sessions_data[id]["session_duration_sum"] / sessions_data[id]["session_count"]
        
        participants_data.append(individual)

    return participants_data

def main():
    with open("sample_data.json", "r") as file:
        data = json.load(file)
    
    # data = requests.get(URL).json()

    rounds = data["rounds"]
    sessions = data["sessions"]
    participants = data["participantInfo"]

    rounds_data = process_rounds(rounds)
    sessions_data, languages = process_sessions(sessions, rounds_data)
    participants_data = aggregate_by_participant(participants, sessions_data)
    print(languages)
    # print(participants_data)

if __name__ == "__main__":
    main()