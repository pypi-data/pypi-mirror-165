# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['czech_holidays']
install_requires = \
['python-dateutil']

setup_kwargs = {
    'name': 'czech-holidays',
    'version': '1.0.0',
    'description': 'Python package with Czech public holidays',
    'long_description': '\nCzech Holidays\n==============\n\nPython package with `Czech public holidays <https://en.wikipedia.org/wiki/Public_holidays_in_the_Czech_Republic>`_.\n\nInstallation\n------------\n\nFrom PyPI::\n\n    pip install czech-holidays\n\nIn case you have an adventurous mind, give a try to the source::\n\n    pip install git+https://github.com/honzajavorek/czech-holidays.git#egg=czech-holidays\n\nExamples\n--------\n\nCzech Holidays provides the following interface:\n\n.. code:: python\n\n    >>> from czech_holidays import czech_holidays\n    >>> holidays = czech_holidays(2022)\n    >>> holidays[:3]\n    [Holiday(date=datetime.date(2022, 1, 1), name=\'Nový rok\', name_en="New Year\'s Day"),\n     Holiday(date=datetime.date(2022, 1, 1), name=\'Den obnovy samostatného českého státu\', name_en=\'Restoration Day of the Independent Czech State\'),\n     Holiday(date=datetime.date(2022, 4, 18), name=\'Velikonoční pondělí\', name_en=\'Easter Monday\')]\n\nThe function accepts year as a single argument and returns a list of `named tuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:\n\n.. code:: python\n\n    >>> holidays[0].date\n    datetime.date(2022, 1, 1)\n    >>> holidays[0].name\n    \'Nový rok\'\n    >>> holidays[0].name_en\n    "New Year\'s Day"\n\nAlbeit named, it\'s still just a tuple:\n\n.. code:: python\n\n    >>> holidays[0][0]\n    datetime.date(2022, 1, 1)\n    >>> holidays[0][1]\n    \'Nový rok\'\n    >>> holidays[0][2]\n    "New Year\'s Day"\n    >>> tuple(holidays[0])\n    (datetime.date(2022, 1, 1), \'Nový rok\', "New Year\'s Day")\n    >>> holidays[0] < holidays[5]\n    True\n\nTwo shortcuts are available:\n\n.. code:: python\n\n    >>> from czech_holidays import czech_easter, czech_christmas\n    >>> czech_easter(2022)\n    Holiday(date=datetime.date(2022, 4, 18), name=\'Velikonoční pondělí\', name_en=\'Easter Monday\')\n    >>> czech_christmas(2022)\n    Holiday(date=datetime.date(2022, 12, 24), name=\'Štědrý den\', name_en=\'Christmas Eve\')\n\nThe aim of this library is to simplify work with Czech public holidays in current\napplications, thus **it does not provide any historical data**:\n\n.. code:: python\n\n    >>> czech_holidays(2013)\n    Traceback (most recent call last):\n    NotImplementedError: ...\n\nDevelopment\n-----------\n\nInstall using `poetry <https://python-poetry.org/>`_::\n\n    git clone git@github.com:honzajavorek/czech-holidays.git\n    cd czech-holidays\n    poetry install\n\nThen run tests::\n\n    pytest\n\nLicense: MIT\n------------\n\n© 2022 Honza Javorek <mail@honzajavorek.cz>\n\nThis work is licensed under `MIT license <https://en.wikipedia.org/wiki/MIT_License>`_.\n',
    'author': 'Honza Javorek',
    'author_email': 'mail@honzajavorek.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/honzajavorek/czech-holidays',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
