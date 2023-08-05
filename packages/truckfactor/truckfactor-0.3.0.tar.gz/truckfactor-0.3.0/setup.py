# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truckfactor']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'numpy>=1.19.4,<2.0.0', 'pandas>=1.1.5,<2.0.0']

entry_points = \
{'console_scripts': ['truckfactor = truckfactor.compute:run']}

setup_kwargs = {
    'name': 'truckfactor',
    'version': '0.3.0',
    'description': ' Tool to compute the truck factor of a Git repository ',
    'long_description': '![](artwork/logo.png)\n\n# What is this?\n\nThis tool, `truckfactor` computes the \n[truck (bus/lorry/lottery) factor](https://en.wikipedia.org/wiki/Bus_factor) for a \ngiven Git repository.\n\nThe truck factor is\n\n  > the number of people on your team that have to be hit by a truck (or quit) \n  > before the project is in serious trouble\n  >\n  > L. Williams and R. Kessler, Pair Programming Illuminated. Addison Wesley, 2003.\n\n<!-- One of the earliest occurrences of the term in a real project was in the Python\nmailing list: \n["If Guido was hit by a bus?"](https://legacy.python.org/search/hypermail/python-1994q2/1040.html) -->\n\n\n## Installation\n\n```\npip install truckfactor\n```\n\n### Requirements\n\nThe tool requires that `git` is installed and accessible on `PATH`.\n\n\n## How to use it?\n\nYou have to either point the tool to a directory containing a Git repository or\nto a URL with a remote repository. In case a URL is given, the tool will clone\nthe repository into a temporary directory.\n\nFrom the terminal, the tool can be run as in the following:\n\n```\nUsage:\n  truckfactor <repository> [<commit_sha>] [--output=<kind>]\n  truckfactor -h | --help\n  truckfactor --version\n\nOptions:\n  -h --help     Show this screen.\n  --version     Show version.\n  --output=<kind>  Kind of output, either csv or verbose.\n```\n\nFor example, in its most basic form it can be called like this:\n\n```bash\n$ truckfactor <path_or_url_to_repository>\nThe truck factor of <path_to_repository> (<commit_sha>) is: <number>\n```\n\nIf no `output` switch is given, the tool produces a single line output above. Otherwise, it will output a line in CSV format or in key: value form.\n\n\nCalling it from code:\n\n```python\nfrom truckfactor.compute import main\n\n\ntruckfactor, commit_sha, authors = main("<path_to_repo>")\n```\n\n\n# How does the tool compute the truck factor?\n\nIn essence the tool does the following:\n\n  * Reads a git log from the repository\n  * Computes for each file who has the _knowledge ownership_ of it.\n    - A contributor has knowledge ownership of a file when she edited the most \n    lines in it.\n    - That computation is inspired by \n    [A. Thornhill _Your Code as a Crime Scene_](https://pragprog.com/titles/atcrime/your-code-as-a-crime-scene/).\n    - Note, only for text files knowledge ownership is computed. The tool may \n    not return a good answer for repositories containing only binary files.\n  * Then similar to [G. Avelino et al. *A novel approach for estimating Truck Factors*](https://peerj.com/preprints/1233.pdf) \n  low-contributing authors are removed from the analysis as long as still more \n  than half of all files have a knowledge owner. The amount of remaining \n  knowledge owners is the truck factor of the given repository.\n\n\n# Why does it exist?\n\nThis tool was developed since in Dec. 2020, we could not find an open-source and readily installable tool to compute truck factors of projects on PyPI or Rubygems.\n\n<!-- \n## References\n\nhttps://link.springer.com/article/10.1007/s11219-019-09457-2\n\nA novel approach for estimating truck factors.\nhttps://github.com/aserg-ufmg/Truck-Factor\n\nAssessing the Bus Factor of Git Repositories (https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7081864&casa_token=fJYjmp-T3RUAAAAA:o_c0hD_yzQHTQJF0rGtEldCmxWlj_E0qn-NN67dxk4rps-p3fcBKpzzonY5SuFez8NEJ5sEx&tag=1)\nhttps://github.com/atlanmod/busfactor\nhttps://github.com/SOM-Research/busfactor\n   > the minimum number of people on your team who must be hit by a truck so that your project gets into serious trouble (Bowler, M. (2005). Truck factor. Online. http://www.agileadvice.com/2005/05/15/agilemanagement/truck-factor/, )\n\nQuantifying and mitigating turnover-induced knowledge loss: case studies of Chrome and a project at Avaya\n-> no tool available\n\nAre Heroes common in FLOSS projects?\nhttps://dl.acm.org/doi/pdf/10.1145/1852786.1852856?casa_token=zZmr-B41OKYAAAAA:z1z_-tQivlm19DqvLysjT2ZNOwvmCmeU_KqtNBM9I3R2ol7EFbQtxx8nFKe921jQgupkAwPRVtct\non SVN no tool linked\n\n\nOn the difficulty of computing the Truck Factor\nhttps://www.researchgate.net/profile/Filippo_Ricca/publication/221219219_On_the_Difficulty_of_Computing_the_Truck_Factor/links/5746d7db08ae9ace8425ec3e/On-the-Difficulty-of-Computing-the-Truck-Factor.pdf\nSVN no tools linked\n -->\n\n\n\n-----\n\n# Attributions\n\nThe logo is combined from two logos from flaticon:\n  * Truck: <div>Icons made by <a href="https://www.flaticon.com/authors/kiranshastry" title="Kiranshastry">Kiranshastry</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>\n  * Warning sign: <div>Icons made by <a href="https://www.flaticon.com/authors/gregor-cresnar" title="Gregor Cresnar">Gregor Cresnar</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>\n\n\n',
    'author': 'HelgeCPH',
    'author_email': 'ropf@itu.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HelgeCPH/truckfactor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
