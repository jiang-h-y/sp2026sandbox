import requests
from collections import defaultdict

URL = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6ImppYW5nLmhlaUBub3J0aGVhc3Rlcm4uZWR1IiwiZHVlRGF0ZSI6IjIwMjUtMTItMTlUMDU6MDA6MDAuMDAwWiJ9LCJoYXNoIjoiUmhDdUx2SFBub3dYQjZ1M1RCVSJ9"

def group_by_session(rounds):
    """ 
    Groups rounds data by session, keeping only necessary stats
    (total score and duration of each round)

    Ex.
    {
    0: {
        'score_sum': 5.0,
        'round_duration_sum': 100.0
        }
    }
    """
    # initialize necessary stats
    session_stats = defaultdict(lambda: {
        "score_sum": 0.0, 
        "round_duration_sum": 0.0
        })

    for r in rounds:
        # identify which session the round belongs to
        session = session_stats[r["sessionId"]]

        session["score_sum"] += r["score"]
        session["round_duration_sum"] += r["endTime"] - r["startTime"]

    return session_stats

def merge_sessions_data(s, sessions_grouped):
    """
    Updates the data for a particular session (given by s) by adding the data 
    grouped from each round
    """
    session_id = s["sessionId"]
    s.update(sessions_grouped[session_id])

def calculate_participant_stats(participant, s):
    """
    Calculates stats for a particular participant using sessions data (given by s)

    Stats for the given participant:
    * score_sum: total score across all rounds
    * round_count: total number of rounds played
    * session_duration_sum: total duration across all sessions
    """
    participant["score_sum"] += s["score_sum"]
    participant["round_count"] += len(s["rounds"])
    participant["session_duration_sum"] += s["endTime"] - s["startTime"]

def calculate_language_stats(participant_language, s):
    """
    Calculates stats for a particular participant/language pair using sessions 
    data (given by s)

    Stats for the given participant's performance in a particular language:
    * score_sum: total score across all rounds
    * round_duration_sum: total duration across all rounds
    * round_count: total number of rounds played
    """
    participant_language["score_sum"] += s["score_sum"]
    participant_language["round_duration_sum"] += s["round_duration_sum"]
    participant_language["round_count"] += len(s["rounds"])

def group_by_participant(sessions_base, sessions_grouped):
    """ 
    Aggregates sessions data by participant, using the base sessions data and
    the sessions data grouped from each round.

    Returns:
    participant_stats ex.
    Ex.
    {
    0: {
        'score_sum': 10,
        'round_count': 2,
        'session_duration_sum': 200,
        }
    }

    language_stats ex.
    {
    0: {
        "English": {
            'score_sum': 7,
            'round_duration_sum': 150,
            'round_count': 2
            }
        }
    }
    """
    participant_stats = defaultdict(lambda: {
        "score_sum": 0.0, 
        "round_count": 0, 
        "session_duration_sum": 0.0
        })
    language_stats = defaultdict(lambda: defaultdict(lambda: {
        "score_sum": 0.0, 
        "round_duration_sum": 0.0, 
        "round_count": 0
        }))

    for s in sessions_base:
        # merge base data with new data grouped from each round
        merge_sessions_data(s, sessions_grouped)

        # identify which participant the session belongs to
        participant = participant_stats[s["participantId"]]
        calculate_participant_stats(participant, s)

        # identify which participant the language belongs to
        participant = language_stats[s["participantId"]]
        participant_language = participant[s["language"]]
        calculate_language_stats(participant_language, s)

    return participant_stats, language_stats

def flatten_language_stats(language_stats):
    """
    Flattens input by grouping data by participants, then constructing a list of 
    each participant's languages and computing the associated averages;
    matches the desired final 'languages' output shape.

    Ex.
    Original:
    {
    0: {
        "English": {
            'score_sum': 7,
            'round_duration_sum': 150,
            'round_count': 2
            }
        }
    }

    Flattened:
    {
    0: [
            {
            'language': 'English',
            'averageScore': 3.5,
            'averageRoundDuration': 75.0
            }
        ]
    }
    """
    flattened = {}

    for id, languages in language_stats.items():
        flattened[id] = []
        
        for language, vals in languages.items():
            stats = {}
            stats["language"] = language
            stats["averageScore"] = round(vals["score_sum"] / vals["round_count"], 2)
            stats["averageRoundDuration"] = round(vals["round_duration_sum"] / vals["round_count"], 2)
            flattened[id].append(stats)
    
    return flattened

def merge_participants_data(p, participants_grouped):
    """
    Updates the data for a particular participant (given by p) by adding the data 
    grouped from each session
    """
    participant_id = p["participantId"]
    p.update(participants_grouped[participant_id])

def aggregate_participant_stats(p, languages_data):
    """ 
    For a particular participant (given by p), aggregates languages data,
    average round score, and average session duration into one dictionary.
    
    Returns an empty list for languages and 'N/A' for the other stats if the
    participant has not played any rounds.
    """
    sessions_count = len(p["sessions"])

    if sessions_count > 0:
        return {
            "languages": languages_data,
            "averageRoundScore": round(p["score_sum"] / p["round_count"], 2),
            "averageSessionDuration": round(p["session_duration_sum"] / sessions_count, 2)
        }
    
    return {
        "languages": languages_data,
        "averageRoundScore": "N/A",
        "averageSessionDuration": "N/A"
    }

def sort_list_of_dicts(lst):
    """ Sorts a list of dictionaries in alphabetical order based on name """
    return sorted(lst, key=lambda dct: dct["name"])

def format_output(participants, participants_grouped, languages):
    """ Formats output to structure it like the example """
    output = []

    for p in participants:
        merge_participants_data(p, participants_grouped)
        id = p["participantId"]
        data = {}
        data["id"] = id
        data["name"] = p["name"]
        data.update(aggregate_participant_stats(p, languages.get(id, [])))
        
        output.append(data)

    output = sort_list_of_dicts(output)
    return output 

def main():
    # load data
    data = requests.get(URL).json()

    # identify separate parts of the data for readability
    rounds = data["rounds"]
    sessions = data["sessions"]
    participants = data["participantInfo"]

    # group rounds data by session, then sessions data by participants
    session_stats = group_by_session(rounds)
    participant_stats, language_stats = group_by_participant(sessions, session_stats)

    # make languages data easier to use
    flattened_language = flatten_language_stats(language_stats)

    output = format_output(participants, participant_stats, flattened_language)
    import pprint
    pprint.pprint(output)

if __name__ == "__main__":
    main()