# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysubparser',
 'pysubparser.classes',
 'pysubparser.cleaners',
 'pysubparser.parsers',
 'pysubparser.writers']

package_data = \
{'': ['*']}

install_requires = \
['unidecode>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'pysub-parser',
    'version': '1.7.0',
    'description': 'Utility to extract the contents of a subtitle file.',
    'long_description': "## pysub-parser\n\n[![Version](https://img.shields.io/pypi/v/pysub-parser?logo=pypi)](https://pypi.org/project/pysub-parser)\n[![Quality Gate Status](https://img.shields.io/sonar/alert_status/fedecalendino_pysub-parser?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_pysub-parser)\n[![CodeCoverage](https://img.shields.io/sonar/coverage/fedecalendino_pysub-parser?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_pysub-parser)\n\nUtility to extract the contents of a subtitle file.\n\nSupported types:\n\n* `ass`: [Advanced SubStation Alpha](https://en.wikipedia.org/wiki/SubStation_Alpha#Advanced_SubStation_Alpha)\n* `ssa`: [SubStation Alpha](https://en.wikipedia.org/wiki/SubStation_Alpha)\n* `srt`: [SubRip](https://en.wikipedia.org/wiki/SubRip)\n* `sub`: [MicroDVD](https://en.wikipedia.org/wiki/MicroDVD)\n* `txt`: [Sub Viewer](https://en.wikipedia.org/wiki/SubViewer)\n\n> For more information: http://write.flossmanuals.net/video-subtitling/file-formats\n\n### Usage\n\nThe method parse requires the following parameters:\n\n* `path`: location of the subtitle file.\n* `subtype`: one of the supported file types, by default file extension is used.\n* `encoding`: encoding of the file, `utf-8` by default.\n* `**kwargs`: optional parameters.\n  * `fps`: framerate (only used by `sub` files), `23.976` by default.\n\n```python\nfrom pysubparser import parser\n\nsubtitles = parser.parse('./files/space-jam.srt')\n\nfor subtitle in subtitles:\n    print(subtitle)\n```\n\nOutput:\n```text\n0 > [BALL BOUNCING]\n1 > Michael?\n2 > What are you doing out here, son? It's after midnight.\n3 > MICHAEL: Couldn't sleep, Pops.\n```\n\n___\n\n### Subtitle Class\n\nEach line of a dialogue is represented with a `Subtitle` object with the following properties:\n\n* `index`: position in the file.\n* `start`: timestamp of the start of the dialog.\n* `end`: timestamp of the end of the dialog.\n* `text`: dialog contents.\n\n```python\nfor subtitle in subtitles:\n    print(f'{subtitle.start} > {subtitle.end}')\n    print(subtitle.text)\n    print()\n```\n\nOutput:\n```text\n00:00:36.328000 > 00:00:38.329000\n[BALL BOUNCING]\n\n00:01:03.814000 > 00:01:05.189000\nMichael?\n\n00:01:08.402000 > 00:01:11.404000\nWhat are you doing out here, son? It's after midnight.\n\n00:01:11.572000 > 00:01:13.072000\nMICHAEL: Couldn't sleep, Pops.\n```\n\n### Cleaners\n\nCurrently, 4 cleaners are provided:\n\n* `ascii` will translate every unicode character to its ascii equivalent.\n* `brackets` will remove anything between them (e.g., `[BALL BOUNCING]`)\n* `formatting` will remove formatting keys like `<i>` and `</i>`.\n* `lower_case` will lower case all text. \n\n```python\nfrom pysubparser.cleaners import ascii, brackets, formatting, lower_case\n\nsubtitles = brackets.clean(\n    lower_case.clean(\n        subtitles\n    )\n)\n\nfor subtitle in subtitles:\n    print(subtitle)\n```\n\n```text\n0 > \n1 > michael?\n2 > what are you doing out here, son? it's after midnight.\n3 > michael: couldn't sleep, pops.\n```\n\n### Writers\n\nGiven any list of `Subtitle` and a path it will output those subtitles in a `srt` format.\n",
    'author': 'Fede Calendino',
    'author_email': 'fede@calendino.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedecalendino/pysub-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
