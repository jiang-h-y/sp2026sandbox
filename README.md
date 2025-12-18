## Data Definition
Full input data: `dict[str, list]`

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

I understand that these diagrams are not ideal for modeling JSON data because there are different restrictions and structures for JSON vs relational databases. However, it was helpful for me to visually see the data represented in this way.

<img width="1260" height="1288" alt="image" src="https://github.com/user-attachments/assets/dcdc068a-059c-495f-8ef2-b8cb06a8f22f" />

## How to run my solution
Run: `main.py` (may need to install `requirements.txt`)

Repo structure:  
`test_main.py`: tests for my solution  
`\test_data`: data for testing  
`\archive`: previous versions of my solution  
`\diagrams`: ER/relational diagram drawings 

## Thought process
After drawing out the relational diagrams, I looked at the foreign key relationships and realized I could take a bottom-up approach with aggregating the data in these steps:

1. Iterate through the rounds data and aggregate it by session.
2. Iterate through the sessions data and aggregate it by participant.
3. Process and format all the data.

I thought this was the best way to approach the problem because it handled each part of the data (sessions, rounds, participants) separately and avoided extremely nested for loops in which I would have to iterate over multiple parts of the data simultaneously.

Although I never took the Fundies track, I know some of the most basic design principles about making each function do only one job and avoiding repitive code. For my first attempt at implementing my solution, I iterated through each part of the data once and performed my aggregations/computations. However, this version was extremely unreadable, and the functions were not as modular as I wanted them to be.

I redesigned the solution twice to make it more readable and modular by separating out the tasks into smaller steps. For example, I added a function just for processing the languages data. This did require me to perform additional iterations through the data, which sacrificed some efficiency. I thought this sacrifice was necessary because of the more important improvements in readability and modularity. In total, this challenge took me around 15 hours.

## Technical challenges
The two biggest technical challenges I faced were:
1. Deciding on the right data structure to use
2. Unit testing

In the intermediary steps of data processing, I had to decide how to store my data. I mostly used default dictionaries to store my intermediary data because dictionary keys must be unique. This allowed me to make each ID a unique key and aggregate data as the values for the keys. Furthermore, dictionaries allow for quick and easy access to data. The reason I used default dictionaries was to avoid the extra step of making an if-else statement to check if the ID was already in the dictionary.

However, deciding on this data structure was extremely difficult for me because the data became very nested, which was difficult to understand and work with. I'm also used to working with data science projects where the data is typically organized as a dataframe, so this hierarchical structure was new to me. 

I thought about using alternative data structures, such as a dictionary of lists instead of a dictionary of dictionaries. This would reduce the readability of the data because there would be no names attributed to each value (e.g. [5, 100] instead of {"score": 5, "duration": 100}). I also thought about designing the data structure as a list of dictionaries, where the index in the list corresponded to the data's ID and the dictionaries provided the values. This was difficult to implement too because the data is not given in order of ID, so you have to pre-define a list of a certain length for this to work. Therefore, I ultimately decided that dictionaries with ID keys were the best possible data structure I could think of.

Unit testing was difficult for me as well because I don't have much practice with it. As I was writing my tests, I felt like my inputs and outputs were extremely complicated and cumbersome, and it made me lose confidence in my solution. On the other hand, writing tests did help me realize that I could break down some of my functions into smaller functions, so I revised my solution several times during the testing process. I'm still not sure if I did my testing correctly because the tests seemed overly complicated, but I just tried to test every function and get as much coverage as possible.

## Sources referenced for my code:

https://www.geeksforgeeks.org/python/get-post-requests-using-python/
https://stackoverflow.com/questions/2600790/multiple-levels-of-collection-defaultdict-in-python
https://stackoverflow.com/questions/71679139/python-defaultdict-with-defined-dictionary-as-default-value-shares-the-same-dict
https://stackoverflow.com/questions/31168819/how-to-send-an-array-using-requests-post-python-value-error-too-many-values
https://stackoverflow.com/questions/4183506/python-list-sort-in-descending-order
https://www.w3schools.com/python/ref_requests_response.asp
