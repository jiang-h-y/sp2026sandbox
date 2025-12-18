import pytest
from main import *
import json

def test_group_by_session():
    # no rounds data
    rounds1 = []
    solution1 = {}
    assert group_by_session(rounds1) == solution1

    # multiple rounds for different sessions
    rounds2 = [
    {"sessionId": 0, "score": 7, "startTime": 100, "endTime": 200},
    {"sessionId": 1, "score": 2, "startTime": 100, "endTime": 800}
    ]
    solution2 = {
    0: {"score_sum": 7, "round_duration_sum": 100},
    1: {"score_sum": 2, "round_duration_sum": 700}
    }
    assert group_by_session(rounds2) == solution2

    # multiple rounds for the same session
    rounds3 = [
    {"sessionId": 0, "score": 7, "startTime": 100, "endTime": 200},
    {"sessionId": 0, "score": 2, "startTime": 100, "endTime": 800}
    ]
    solution3 = {
    0: {"score_sum": 9, "round_duration_sum": 800}
    }
    assert group_by_session(rounds3) == solution3

def test_update_data():
    # no base data
    ID = "id"
    base1 = []
    new1 = {}
    solution1 = []
    assert update_data(base1, new1, ID) == solution1

    # no new data
    base2 = [{"id": 0, "number": 1, "letter": "a"}]
    new2 = {}
    assert update_data(base2, new2, ID) == base2

    # standard data
    base3 = [{"id": 0, "number": 1, "letter": "a"}]
    new3 = {0: {"color": "blue"}, 1: {"color": "green"}}
    solution3 = [{"id": 0, "number": 1, "letter": "a", "color": "blue"}]
    assert update_data(base3, new3, ID) == solution3

def test_group_by_participant():
    # no sessions data
    sessions1 = []
    solution1 = {}
    assert group_by_participant(sessions1) == solution1

    # multiple sessions for different participants
    sessions2 = [
    {"participantId": 0, "rounds": [0, 1], "score_sum": 7, "startTime": 100, "endTime": 200},
    {"participantId": 1, "rounds": [2], "score_sum": 2, "startTime": 100, "endTime": 800}
    ]
    solution2 = {
    0: {"score_sum": 7, "round_count": 2, "session_duration_sum": 100},
    1: {"score_sum": 2, "round_count": 1, "session_duration_sum": 700}
    }
    assert group_by_participant(sessions2) == solution2

    # multiple sessions for the same participant
    sessions3 = [
    {"participantId": 0, "rounds": [0, 1], "score_sum": 7, "startTime": 100, "endTime": 200},
    {"participantId": 0, "rounds": [2], "score_sum": 2, "startTime": 100, "endTime": 800}
    ]
    solution3 = {
    0: {"score_sum": 9, "round_count": 3, "session_duration_sum": 800}
    }
    assert group_by_participant(sessions3) == solution3

def test_group_by_participant_language():
    # no sessions data
    sessions1 = []
    solution1 = {}
    assert group_by_participant_language(sessions1) == solution1

    # multiple languages for the same participant
    sessions2 = [
    {"participantId": 0, "language": "English", "rounds": [0, 1], "score_sum": 10, "round_duration_sum": 200},
    {"participantId": 0, "language": "French", "rounds": [2], "score_sum": 5, "round_duration_sum": 100}
    ]
    solution2 = {
    0: {
        "English": {"score_sum": 10, "round_duration_sum": 200, "round_count": 2},
        "French": {"score_sum": 5, "round_duration_sum": 100, "round_count": 1}
    }
    }
    assert group_by_participant_language(sessions2) == solution2

    # multiple participants with the same language
    sessions3 = [
    {"participantId": 0, "language": "English", "rounds": [0], "score_sum": 7, "round_duration_sum": 150},
    {"participantId": 1, "language": "French", "rounds": [1, 2], "score_sum": 12, "round_duration_sum": 300}
    ]
    solution3 = {
    0: {
        "English": {"score_sum": 7, "round_duration_sum": 150, "round_count": 1}
    },
    1: {
        "French": {"score_sum": 12, "round_duration_sum": 300, "round_count": 2}
    }
    }
    assert group_by_participant_language(sessions3) == solution3

def test_sort_languages():
    # no languages data
    languages1 = {}
    assert sort_languages(languages1) == languages1

    # standard data
    languages2 = {"English": {"score_sum": 50.0}, "Japanese": {"score_sum": 68.0}}
    solution2 = ["Japanese", "English"]
    # dictionary equality doesn"t check for order
    assert list(sort_languages(languages2).keys()) == solution2

def test_flatten_languages():
    # no languages data
    languages1 = {}
    solution1 = []
    assert flatten_languages(languages1) == solution1

    # standard data
    languages2 = {
        'English': {'score_sum': 7, 'round_duration_sum': 150, 'round_count': 2},
        'French': {'score_sum': 5, 'round_duration_sum': 200, 'round_count': 2}
    }
    solution2 = [
        {'language': 'English', 'averageScore': 3.5, 'averageRoundDuration': 75.0},
        {'language': 'French', 'averageScore': 2.5, 'averageRoundDuration': 100.0}
    ]
    assert flatten_languages(languages2) == solution2

def test_format_language_stats():
    # no language stats data
    language_stats1 = {}
    assert format_language_stats(language_stats1) == language_stats1

    # standard data
    language_stats2 = {
    0: {
        'French': {'score_sum': 5, 'round_duration_sum': 200, 'round_count': 2},
        "English": {'score_sum': 7, 'round_duration_sum': 150, 'round_count': 2}
        }
    }
    solution2 = {
    0: [
            {'language': 'English', 'averageScore': 3.5, 'averageRoundDuration': 75.0},
            {'language': 'French', 'averageScore': 2.5, 'averageRoundDuration': 100.0}
        ]
    }
    assert format_language_stats(language_stats2) == solution2

def test_aggregate_participant_stats():
    # no sessions data
    p1 = {"participantId": 0, "sessions": []}
    languages1 = {}
    solution1 = {"languages": [], "averageRoundScore": "N/A", "averageSessionDuration": "N/A"}
    assert aggregate_participant_stats(p1, languages1) == solution1

    # standard data
    p2 = {"participantId": 0, "sessions": [0], "score_sum": 50, "round_count": 10, "session_duration_sum": 300}
    languages2 = {0: [{"language": "German", "averageRoundScore": 5, "averageRoundDuration": 100}]}
    solution2 = {
        "languages": languages2[p2["participantId"]],
        "averageRoundScore": round(50 / 10, 2),
        "averageSessionDuration": round(300 / 1, 2)
    }
    assert aggregate_participant_stats(p2, languages2) == solution2

def test_sort_participants():
    # no participants data
    participants1 = []
    assert sort_participants(participants1) == participants1

    # standard data
    participants2 = [{"name": "Delta"}, {"name": "Bravo"}]
    solution2 = [{"name": "Bravo"}, {"name": "Delta"}]
    assert sort_participants(participants2) == solution2

    # already sorted
    participants3 = [{"name": "Alpha"}, {"name": "Bravo"}]
    assert sort_participants(participants3) == participants3

def test_end_to_end():
    """ Tests the end-to-end pipeline using the given sample data/solution """
    with open("sample_data.json", "r") as file:
        data = json.load(file)

    with open("sample_solution.json", "r") as file:
        solution = json.load(file)
    
    rounds = data["rounds"]
    sessions = data["sessions"]
    participants = data["participantInfo"]

    output = process_data(rounds, sessions, participants)
    assert output == solution

if __name__ == "__main__":
    pytest.main()