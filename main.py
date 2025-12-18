import requests
from collections import defaultdict
import copy

URL = "https://recruitment.sandboxnu.com/api/eyJkYXRhIjp7ImNoYWxsZW5nZSI6IkZsb3ciLCJlbWFpbCI6ImppYW5nLmhlaUBub3J0aGVhc3Rlcm4uZWR1IiwiZHVlRGF0ZSI6IjIwMjUtMTItMTlUMDU6MDA6MDAuMDAwWiJ9LCJoYXNoIjoiUmhDdUx2SFBub3dYQjZ1M1RCVSJ9"

def group_by_session(rounds):
    """ 
    Groups rounds data by session, keeping only necessary stats
    (total score and duration of each round)

    Ex.
    {
    0: {
        'score_sum': 5,
        'round_duration_sum': 100
        }
    }
    """
    # initializes necessary stats
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

def update_data(base, new, id_key):
    """ 
    Adds new data to existing data based on an ID key

    Ex.
    base:
    [{'id': 0, 'number': 1, 'letter': 'a'}]

    new:
    {0: {'color': 'blue'}, 1: {'color': 'green'}}

    updated:
    [{'id': 0, 'number': 1, 'letter': 'a', 'color': 'blue'}]
    """
    # in case of no base data
    if len(base) == 0:
        return []

    # avoid directly modifying the original data
    updated = copy.deepcopy(base)

    for u in updated:
        u_id = u[id_key]
        # add new data if it exists
        u.update(new.get(u_id, {}))

    return updated

def group_by_participant(sessions):
    """ 
    Groups sessions data by participant, keeping only necessary stats
    (total round score, round count, total session duration)

    Ex.
    {
    0: {
        'score_sum': 10,
        'round_count': 2,
        'session_duration_sum': 200,
        }
    }
    """
    # initializes necessary stats
    participant_stats = defaultdict(lambda: {
        "score_sum": 0.0, 
        "round_count": 0, 
        "session_duration_sum": 0.0
        })

    for s in sessions:
        # identify which participant the session belongs to
        participant = participant_stats[s["participantId"]]

        participant["score_sum"] += s["score_sum"]
        participant["round_count"] += len(s["rounds"])
        participant["session_duration_sum"] += s["endTime"] - s["startTime"]
    
    return participant_stats

def group_by_participant_language(sessions):
    """
    Groups sessions data by participant and language, keeping only necessary stats
    (total round score, total round duration, round count)
    
    Ex.
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
    # initializes necessary stats
    language_stats = defaultdict(lambda: defaultdict(lambda: {
        "score_sum": 0.0, 
        "round_duration_sum": 0.0, 
        "round_count": 0
        }))

    for s in sessions:
        # identify which participant/language pair the session belongs to
        participant = language_stats[s["participantId"]]
        language = participant[s["language"]]

        language["score_sum"] += s["score_sum"]
        language["round_duration_sum"] += s["round_duration_sum"]
        language["round_count"] += len(s["rounds"])

    return language_stats

def sort_languages(dct):
    """ 
    Sort a dictionary of language dictionaries based on total score (in
    descending order)
    """
    return dict(sorted(dct.items(), key=lambda item: item[1]["score_sum"], reverse=True))

def flatten_languages(languages):
    """
    Flattens languages (dictionary of dictionaries) so that it becomes a list
    of dictionaries in which the language keys are converted into dictionary
    values.

    Ex.
    Original:
    {
        'English': {
            'score_sum': 7,
            'round_duration_sum': 150,
            'round_count': 2
            },
        'French': {
            'score_sum': 5,
            'round_duration_sum': 200,
            'round_count': 2
            }
    }

    Flattened:
    [
        {
        'language': 'English',
        'averageScore': 3.5,
        'averageRoundDuration': 75.0
        },
        {
        'language': 'French',
        'averageScore': 2.5,
        'averageRoundDuration': 100.0
        }
    ]
    """

    flattened_lst = []

    for language, stats in languages.items():
        flattened = {}
        flattened["language"] = language
        flattened["averageScore"] = round(stats["score_sum"] / stats["round_count"], 2)
        flattened["averageRoundDuration"] = round(stats["round_duration_sum"] / stats["round_count"], 2)
        flattened_lst.append(flattened)
    
    return flattened_lst

def format_language_stats(language_stats):
    """
    Formats language stats so that it matches the desired final 'languages' 
    output shape.

    Ex.
    Original:
    {
    0: {
        'French': {
            'score_sum': 5,
            'round_duration_sum': 200,
            'round_count': 2
            },
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
            },
            {
            'language': 'French',
            'averageScore': 2.5,
            'averageRoundDuration': 100.0
            }
        ]
    }
    """
    formatted = {}

    for id, languages in language_stats.items():
        # sort data based on specifications
        languages = sort_languages(languages)

        # add languages data for each participant ID
        formatted[id] = flatten_languages(languages)
    
    return formatted

def aggregate_participant_stats(p, languages):
    """ 
    For a particular participant (given by p), aggregates languages data,
    average round score, and average session duration into one dictionary.
    
    Returns an empty list for languages and 'N/A' for the other stats if the
    participant has not played any rounds.
    """
    sessions_count = len(p["sessions"])

    if sessions_count > 0:
        return {
            "languages": languages[p["participantId"]],
            "averageRoundScore": round(p["score_sum"] / p["round_count"], 2),
            "averageSessionDuration": round(p["session_duration_sum"] / sessions_count, 2)
        }
    
    # handles users who have not played any sessions
    return {
        "languages": [],
        "averageRoundScore": "N/A",
        "averageSessionDuration": "N/A"
    }

def sort_participants(lst):
    """ 
    Sorts a list of participant dictionaries in alphabetical order based on name 
    """
    return sorted(lst, key=lambda dct: dct["name"])

def format_output(participants, languages):
    """ 
    Formats the output according to the desired output format/shape
    """
    output = []

    for p in participants:
        p_id = p["participantId"]
        data = {}
        data["id"] = p_id
        data["name"] = p["name"]
        data.update(aggregate_participant_stats(p, languages))
        
        output.append(data)

    output = sort_participants(output)
    return output  

def process_data(rounds, sessions, participants):
    """ 
    Peforms computations and aggregations on the data to turn it into the
    desired output; takes a bottom-up approach that:
    1. Groups rounds data by session
    2. Groups sessions data by participant
    3. Formats and aggregates the data
    """
    # group rounds data by session and add to existing sessions data
    sessions_stats = group_by_session(rounds)
    updated_sessions = update_data(sessions, sessions_stats, "sessionId")

    # group sessions data by participant and participant/language
    participant_stats = group_by_participant(updated_sessions)
    language_stats = group_by_participant_language(updated_sessions)

    # add new participants data to existing data
    updated_participants = update_data(participants, participant_stats, "participantId")

    # make languages data easier to use
    formatted_language = format_language_stats(language_stats)

    output = format_output(updated_participants, formatted_language)
    return output

def main():
    # load data
    data = requests.get(URL).json()

    # identify separate parts of the data
    rounds = data["rounds"]
    sessions = data["sessions"]
    participants = data["participantInfo"]

    output = process_data(rounds, sessions, participants)

    response = requests.post(url=URL, json=output)
    print(response, response.text)

if __name__ == "__main__":
    main()