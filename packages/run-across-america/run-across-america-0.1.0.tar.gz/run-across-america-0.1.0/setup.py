# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['run_across_america']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['runaa-cli = run_across_america.cli:main']}

setup_kwargs = {
    'name': 'run-across-america',
    'version': '0.1.0',
    'description': 'Run Across America analysis tools',
    'long_description': '# Run Across America\nPython library to fetch and analyze team and user data from Run Across America.\n\n# Installation\n```\npip install run-across-america\n```\n\n# Usage\nAvailable methods:\n- `user_id(user_code: str)`: Exchanges your user code (from the signup email) for your user id.\n- `user(user_id: str)`: Retrieves information about a user from their `user_id`.\n- `teams(user_id: str)`: Retrieves all the teams a particular user is a member of.\n- `goals(team_id: str)`: Retrieves information about the distance goal for a team.\n- `members(team_id: str)`: Retrieves all the members of a team.\n- `leaderboard(team_id: str)`: Retrieves the current leaderboard of a team.\n- `feed(team_id: str)`: Retrieves all the activities of a team.\n\n## User ID\nExchanges your user code (from the signup email) for your user id. Options:\n- `user_code: str` = The alphanumeric code sent to a user after signup.\n\n### Example\n```\n>>> from run_across_america import RunAcrossAmerica\n>>> client = RunAcrossAmerica()\n>>> user_id: str = client.user_id("HELLO")\n\n"f71f47b9-56b0-4bf9-99cd-fcb9b016d819"\n```\n\n## User\nRetrieves information about a user from their `user_id`. Options:\n- `user_id: str` = The GUID obtaining from exchanging the user code. \n\n### Example\n```\n>>> from run_across_america import RunAcrossAmerica, User\n>>> client = RunAcrossAmerica()\n>>> user: User = client.user("f71f47b9-56b0-4bf9-99cd-fcb9b016d819")\n\nUser(id=\'f71f47b9-56b0-4bf9-99cd-fcb9b016d819\', age=None, created=datetime.datetime(2022, 1, 1, 12, 30, 0, 900000), email=\'test@example.com\', first_name=\'Hello\', gender=None, last_name=\'World\', phone=None, icon=None, code=\'YYSHOEY6\', timezone=\'America/Chicago\', username=\'@hello-world\', state=\'IL\')\n```\n',
    'author': 'Kevin Ramdath',
    'author_email': 'krpent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/minormending/run-across-america',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
