# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wordreference_scraper']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1', 'requests>=2.28.1']

setup_kwargs = {
    'name': 'wordreference-scraper',
    'version': '0.1.1',
    'description': 'Scraping words from wordreference.com',
    'long_description': '# wordreference-scraper\nModule for scraping words in Wordreference.com, from English to Spanish.\n\nMultiple languages soon.\n\n## Usage\n\n\'wordreference-scraper\' is used to scrape words and its meanings from the online dictionary "Wordreference"\n\n### One word\n\n```python\nfrom wordreference_scraper.wordreference_scraper import WordreferenceScraper\n\nwords = [\'get\']\n\nwordreference_scraper_instance = WordreferenceScraper(words)\n\nscraped_words = wordreference_scraper_instance.start()\n\nprint(scraped_words)\n# Dictionary where the keys are the forms of the word\n# and the value is the html of all meanings of that word\n```\n\n### Multiple words\n\n```python\nfrom wordreference_scraper.wordreference_scraper import WordreferenceScraper\n\nwords = [\'puzzle\', \'noise\', \'pencil\']\n\nwordreference_scraper_instance = WordreferenceScraper(words)\n\nscraped_words = wordreference_scraper_instance.start()\n\nprint(scraped_words)\n\n```\n### Selecting sections\nWordreference has multiple sections where shows the multiple meanings of word, such as \'Principal translations\', \'Additional translations\', \'Verbal Locutions\', and \'Compound Forms\'. These are the keys and values for the dictionary of sections to scrape\n\n- principal_translations - Boolean: Section for Principal Translations\n- additional_translations - Boolean: Section for Additional Translations\n- compound_forms - Boolean: Section for Compound Forms\n- locuciones_verbales - Boolean: Section for "Locuciones Verbales"\n\n```python\nfrom wordreference_scraper.wordreference_scraper import WordreferenceScraper\n\nwords = [\'Absolute\', \'Note\', \'Self\']\n\nsections = {\n    \'principal_translations\':True,\n    \'additional_translations\':True,\n    \'compound_forms\':False,\n    \'locuciones_verbales\':False\n}\n\nwordreference_scraper_instance = WordreferenceScraper(words,sections)\n\nscraped_words = wordreference_scraper_instance.start()\n\nprint(scraped_words)\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`wordreference_scraper` was created by Santiago Padron. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`wordreference_scraper` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n\n\n\n\n\n\n',
    'author': 'Santiago Padron',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
