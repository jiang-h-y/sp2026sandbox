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

I also drew ER and relational diagrams to help me better visualize the relationships between different parts of the data. 

I understand that these diagrams are not ideal for modeling JSON data because there are different restrictions and structures for these two data formats. However, it was helpful for me to visually see the data represented in this way.

<img width="1260" height="1288" alt="image" src="https://github.com/user-attachments/assets/dcdc068a-059c-495f-8ef2-b8cb06a8f22f" />

## How to run my solution
Run `main.py`

Repo structure:  
`test_main.py`: tests for my solution  
`\test_data`: data for testing  
`\archive`: previous versions of my solution  
`\diagrams`: ER/relational diagram drawings 

Sources:

https://www.geeksforgeeks.org/python/get-post-requests-using-python/
https://stackoverflow.com/questions/2600790/multiple-levels-of-collection-defaultdict-in-python
https://stackoverflow.com/questions/71679139/python-defaultdict-with-defined-dictionary-as-default-value-shares-the-same-dict
https://stackoverflow.com/questions/31168819/how-to-send-an-array-using-requests-post-python-value-error-too-many-values
https://stackoverflow.com/questions/4183506/python-list-sort-in-descending-order
https://www.w3schools.com/python/ref_requests_response.asp
