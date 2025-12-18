## Data Definition
Full input data: `list[dict]`

The input data contains three dictionaries for: (1) sessions, (2) rounds, and (3) participants.

Sessions: `list[dict[str, str | int | list]]`
| Name          | Interpretation                             | Data Type |
|---------------|--------------------------------------------|-----------|
| participantId | participant ID                             | int       |
| sessionId     | session ID                                 | int       |
| language      | session language                           | string    |
| rounds        | all round IDs associated with this session | list[int] |
| startTime     | session start time                         | int       |
| endTime       | session end time                           | int       |

Rounds: `list[dict[str, int]]`
| Name      | Interpretation                   | Data Type |
|-----------|----------------------------------|-----------|
| roundId   | round ID                         | int       |
| sessionId | session ID                       | int       |
| score     | score associated with this round | int       |
| startTime | round start time                 | int       |
| endTime   | round end time                   | int       |

Participant Info: `list[dict[str, str | int | list]]`
| Name          | Interpretation                                   | Data Type |
|---------------|--------------------------------------------------|-----------|
| participantId | participant ID                                   | int       |
| name          | participant's name                               | string    |
| age           | participant's age                                | int       |
| sessions      | all session IDs associated with this participant | list[int] |

Sources:
https://www.geeksforgeeks.org/python/get-post-requests-using-python/
https://stackoverflow.com/questions/2600790/multiple-levels-of-collection-defaultdict-in-python
https://stackoverflow.com/questions/71679139/python-defaultdict-with-defined-dictionary-as-default-value-shares-the-same-dict
https://stackoverflow.com/questions/31168819/how-to-send-an-array-using-requests-post-python-value-error-too-many-values
https://stackoverflow.com/questions/4183506/python-list-sort-in-descending-order
https://www.w3schools.com/python/ref_requests_response.asp
