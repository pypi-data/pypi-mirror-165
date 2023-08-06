# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['czech_holidays']
install_requires = \
['python-dateutil']

setup_kwargs = {
    'name': 'czech-holidays',
    'version': '0.2.0',
    'description': 'Python package with Czech public holidays',
    'long_description': "\nCzech Holidays\n==============\n\nPython package with `Czech public holidays <https://en.wikipedia.org/wiki/Public_holidays_in_the_Czech_Republic>`_.\n\nInstallation\n------------\n\nFrom PyPI::\n\n    pip install czech-holidays\n\nIn case you have an adventurous mind, give a try to the source::\n\n    pip install git+https://github.com/honzajavorek/czech-holidays.git#egg=czech-holidays\n\nExamples\n--------\n\nCzech Holidays provide simple interface:\n\n.. code:: python\n\n    >>> from czech_holidays import holidays\n    >>> holidays\n    [Holiday(2013, 1, 1), Holiday(2013, 1, 1), Holiday(2013, 4, 1), Holiday(2013, 5, 1), Holiday(2013, 5, 8), Holiday(2013, 7, 5), Holiday(2013, 7, 6), Holiday(2013, 9, 28), Holiday(2013, 10, 28), Holiday(2013, 11, 17), Holiday(2013, 12, 24), Holiday(2013, 12, 25), Holiday(2013, 12, 26)]\n\nTwo shortcuts are available:\n\n.. code:: python\n\n    >>> holidays.easter\n    Holiday(2013, 4, 1)\n    >>> holidays.christmas\n    Holiday(2013, 12, 24)\n\nOtherwise ``holidays`` behaves as an ordinary ``list``. If you need holidays\nfor different year, you can make your own ``Holidays`` object:\n\n.. code:: python\n\n    >>> from czech_holidays import Holidays\n    >>> holidays = Holidays(2020)\n    >>> holidays.easter\n    Holiday(2020, 4, 13)\n\n``Holiday`` object behaves as an ordinary ``datetime.date`` object:\n\n.. code:: python\n\n    >>> from czech_holidays import holidays\n    >>> holiday = holidays[5]  # arbitrary holiday\n    >>> holiday.day\n    5\n    >>> holiday.year\n    2013\n    >>> from datetime import timedelta\n    >>> holidays[5] + timedelta(days=4)\n    datetime.date(2013, 7, 9)\n\nIt also has some extra properties:\n\n.. code:: python\n\n    >>> holiday.name\n    u'Den slovansk\\xfdch v\\u011brozv\\u011bst\\u016f Cyrila a Metod\\u011bje'\n    >>> holiday.name_en\n    u'Saints Cyril and Methodius Day'\n\nAim of this library is to simplify work with Czech public holidays in current\napplications, thus **it does not provide any historical data**. For example,\n*Restoration Day of the Independent Czech State* is celebrated since 2000,\nbut the library returns it also for, let's say, 1978.\n\nDevelopment\n-----------\n\nInstall using `poetry <https://python-poetry.org/>`_::\n\n    git clone git@github.com:honzajavorek/czech-holidays.git\n    cd czech-holidays\n    poetry install\n\nThen run tests::\n\n    pytest\n\nLicense: MIT\n------------\n\n© 2022 Honza Javorek <mail@honzajavorek.cz>\n\nThis work is licensed under `MIT license <https://en.wikipedia.org/wiki/MIT_License>`_.\n",
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
