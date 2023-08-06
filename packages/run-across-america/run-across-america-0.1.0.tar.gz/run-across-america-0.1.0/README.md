# Run Across America
Python library to fetch and analyze team and user data from Run Across America.

# Installation
```
pip install run-across-america
```

# Usage
Available methods:
- `user_id(user_code: str)`: Exchanges your user code (from the signup email) for your user id.
- `user(user_id: str)`: Retrieves information about a user from their `user_id`.
- `teams(user_id: str)`: Retrieves all the teams a particular user is a member of.
- `goals(team_id: str)`: Retrieves information about the distance goal for a team.
- `members(team_id: str)`: Retrieves all the members of a team.
- `leaderboard(team_id: str)`: Retrieves the current leaderboard of a team.
- `feed(team_id: str)`: Retrieves all the activities of a team.

## User ID
Exchanges your user code (from the signup email) for your user id. Options:
- `user_code: str` = The alphanumeric code sent to a user after signup.

### Example
```
>>> from run_across_america import RunAcrossAmerica
>>> client = RunAcrossAmerica()
>>> user_id: str = client.user_id("HELLO")

"f71f47b9-56b0-4bf9-99cd-fcb9b016d819"
```

## User
Retrieves information about a user from their `user_id`. Options:
- `user_id: str` = The GUID obtaining from exchanging the user code. 

### Example
```
>>> from run_across_america import RunAcrossAmerica, User
>>> client = RunAcrossAmerica()
>>> user: User = client.user("f71f47b9-56b0-4bf9-99cd-fcb9b016d819")

User(id='f71f47b9-56b0-4bf9-99cd-fcb9b016d819', age=None, created=datetime.datetime(2022, 1, 1, 12, 30, 0, 900000), email='test@example.com', first_name='Hello', gender=None, last_name='World', phone=None, icon=None, code='YYSHOEY6', timezone='America/Chicago', username='@hello-world', state='IL')
```
