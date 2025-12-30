"""
Sources:
https://stackoverflow.com/questions/32497253/parsing-a-json-and-grouping-contents
https://stackoverflow.com/questions/58833915/when-i-convert-groupby-object-to-dict-the-grouper-objects-are-exhausted
"""

import json
from itertools import groupby

def main():
    with open("test_data/sample_data.json", "r") as file:
        data = json.load(file)
    
    rounds = data["rounds"]
    sessions = data["sessions"]
    participants = data["participantInfo"]

    groups_iter = groupby(rounds, lambda rounds : rounds["sessionId"])
    groups = {k: list(v) for k, v in groups_iter}
    print(groups)

if __name__ == "__main__":
    main()