# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctrlmaniac']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['thehouse = ctrlmaniac.ctrlmaniac']}

setup_kwargs = {
    'name': 'ctrlmaniac',
    'version': '0.2.1',
    'description': "Davide DC's GitHub Readme profile",
    'long_description': '# Davide Di Criscito\n\n```python\nclass CtrlManiac:\n    """CtrlManiac because i overuse the ctrl key."""\n\n    def __init__(self):\n        """My specifications."""\n        self.name = "Davide"\n        self.surname = "Di Criscito"\n        self.nickname = "Dave"\n        self.pronouns = (\n            "He",\n            "Him",\n        )\n\n        self.languages_spoken = ["it_IT", "en_US", "en_GB"]\n\n        self.description = (\n            "I\'m currently an Artisan, soon-to-be a full-stack web developer!"\n        )\n\n        self.website = "https://ctrlmaniac.me"\n\n        self.hobbies = [\n            "coding",\n            "hiking",\n            "photography",\n            "watching movies & TV series",\n            "listening to music",\n            "reading books and manga",\n            "going out with my friends and have fun",\n        ]\n\n        self.coding_languages = [\n            "Python",  # I simply love it\n            "JavaScript",\n        ]\n\n        self.favourite_tools = [\n            "poetry",  # makes it simpler to manage a python project\n            "black",  # chooses a coding style for me and makes my code pretty\n            "isort",  # sorts python imports so that everything is really clear\n            "flake8",  # tells me whether I\'ve made a mistake\n            "pydocstyle",  # helps me write better documentation\n            "yarn",  # I love it for the workspace feature\n            "lerna",  # I use it to manage my monorepos\n            "prettier",  # chooses a coding style for me and makes my code pretty\n        ]\n\n        self.IDEs = [\n            "VScode",  # because it\'s awesome!\n        ]\n\n    def greet(self) -> None:\n        """Say hi."""\n        print(\n            f"Hi! I\'m {self.name} {self.surname}, but you can call me {self.nickname}."\n        )\n        print(self.description)\n        print(f"You can know more about me by visiting my website: {self.website}")\n\n    def learn_new_coding_languange(self, language) -> None:\n        """Print a string that tells what new coding language I\'m learning.\n\n        :param language: the coding language to learn.\n        """\n        print(f"I\'m studying a new coding language: {language}")\n```\n\n## Fun Facts\n\nYou can install this package via pip by running `pip install ctrlmaniac` and then excecute the program by typing into your terminal `python -m ctrlmaniac` and see the output!\n\nOr import the package:\n\n```\n>>> from ctrlmaniac import ctrlmaniac\n>>> me = ctrlmaniac.CtrlManiac()\n\n>>> me.greet()\nHi! I\'m Davide Di Criscito, but you can call me Dave.\nI\'m currently an Artisan, soon-to-be a full-stack web developer!\nYou can know more about me by visiting my website: https://ctrlmaniac.me\n\n>>> me.learn_new_coding_languange("Java")\nI\'m studying a new coding language: Java\n\n>>> me.learn_new_coding_languange("Typescript")\nI\'m studying a new coding language: Typescript\n```\n\n## Follow Me on:\n\n- [Twitter](https://twitter.com/ctrlmaniac)\n- [Instagram](https://instagram.com/meldinco)\n- [Linkedin](https://www.linkedin.com/in/dcdavide/)\n- [Pinterest](https://pin.it/4erq4kP)\n\n## :pray: Help me test The House!\n\nHelp me test my text-based game written in python!\nYou can find the repository [here](https://github.com/ctrlmaniac/the-house) or you can install it via pip `pip install thehouse` and then run `thehouse` to make the game start!\n\n## Stats\n\n[![Anurag\'s GitHub stats](https://github-readme-stats.vercel.app/api?username=ctrlmaniac)](https://github.com/anuraghazra/github-readme-stats)\n[![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=ctrlmaniac)](https://github.com/anuraghazra/github-readme-stats)\n',
    'author': 'Davide Di Criscito',
    'author_email': 'davide.dicriscito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
