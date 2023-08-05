# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['klib', 'klib.scripts']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'matplotlib>=3.0.3,<4.0.0',
 'numpy>=1.16.3,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'scipy>=1.1.0,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'klib',
    'version': '1.0.2',
    'description': 'Customized data preprocessing functions for frequent tasks.',
    'long_description': '<p align="center"><img src="https://raw.githubusercontent.com/akanz1/klib/main/examples/images/header.png" alt="klib Header" width="859" height="304"></p>\n\n[![Flake8 & PyTest](https://github.com/akanz1/klib/workflows/Flake8%20%F0%9F%90%8D%20PyTest%20%20%20%C2%B4/badge.svg)](https://github.com/akanz1/klib)\n[![Language](https://img.shields.io/github/languages/top/akanz1/klib)](https://pypi.org/project/klib/)\n[![Last Commit](https://badgen.net/github/last-commit/akanz1/klib/main)](https://github.com/akanz1/klib/commits/main)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=akanz1_klib&metric=alert_status)](https://sonarcloud.io/dashboard?id=akanz1_klib)\n[![Scrutinizer](https://scrutinizer-ci.com/g/akanz1/klib/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/akanz1/klib/)\n[![codecov](https://codecov.io/gh/akanz1/klib/branch/main/graph/badge.svg)](https://codecov.io/gh/akanz1/klib)\n\n**klib** is a Python library for importing, cleaning, analyzing and preprocessing data. Explanations on key functionalities can be found on [Medium / TowardsDataScience](https://medium.com/@akanz) in the [examples](examples) section or on [YouTube (Data Professor)](https://www.youtube.com/watch?v=URjJVEeZxxU).\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install klib.\n\n[![PyPI Version](https://img.shields.io/pypi/v/klib)](https://pypi.org/project/klib/)\n[![Downloads](https://pepy.tech/badge/klib/month)](https://pypi.org/project/klib/)\n\n```bash\npip install -U klib\n```\n\nAlternatively, to install this package with conda run:\n\n[![Conda Version](https://img.shields.io/conda/vn/conda-forge/klib)](https://anaconda.org/conda-forge/klib)\n[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/klib.svg)](https://anaconda.org/conda-forge/klib)\n\n```bash\nconda install -c conda-forge klib\n```\n\n## Usage\n\n```python\nimport klib\nimport pandas as pd\n\ndf = pd.DataFrame(data)\n\n# klib.describe - functions for visualizing datasets\n- klib.cat_plot(df) # returns a visualization of the number and frequency of categorical features\n- klib.corr_mat(df) # returns a color-encoded correlation matrix\n- klib.corr_plot(df) # returns a color-encoded heatmap, ideal for correlations\n- klib.dist_plot(df) # returns a distribution plot for every numeric feature\n- klib.missingval_plot(df) # returns a figure containing information about missing values\n\n# klib.clean - functions for cleaning datasets\n- klib.data_cleaning(df) # performs datacleaning (drop duplicates & empty rows/cols, adjust dtypes,...)\n- klib.clean_column_names(df) # cleans and standardizes column names, also called inside data_cleaning()\n- klib.convert_datatypes(df) # converts existing to more efficient dtypes, also called inside data_cleaning()\n- klib.drop_missing(df) # drops missing values, also called in data_cleaning()\n- klib.mv_col_handling(df) # drops features with high ratio of missing vals based on informational content\n- klib.pool_duplicate_subsets(df) # pools subset of cols based on duplicates with min. loss of information\n```\n\n## Examples\n\nFind all available examples as well as applications of the functions in **klib.clean()** with detailed descriptions <a href="https://github.com/akanz1/klib/tree/main/examples">here</a>.\n\n```python\nklib.missingval_plot(df) # default representation of missing values in a DataFrame, plenty of settings are available\n```\n\n<p align="center"><img src="https://raw.githubusercontent.com/akanz1/klib/main/examples/images/example_mv_plot.png" alt="Missingvalue Plot Example" width="1000" height="1091"></p>\n\n```python\nklib.corr_plot(df, split=\'pos\') # displaying only positive correlations, other settings include threshold, cmap...\nklib.corr_plot(df, split=\'neg\') # displaying only negative correlations\n```\n\n<p align="center"><img src="https://raw.githubusercontent.com/akanz1/klib/main/examples/images/example_corr_plot.png" alt="Corr Plot Example" width="720" height="338"></p>\n\n```python\nklib.corr_plot(df, target=\'wine\') # default representation of correlations with the feature column\n```\n\n<p align="center"><img src="https://raw.githubusercontent.com/akanz1/klib/main/examples/images/example_target_corr_plot.png" alt="Target Corr Plot Example" width="720" height="600"></p>\n\n```python\nklib.dist_plot(df) # default representation of a distribution plot, other settings include fill_range, histogram, ...\n```\n\n<p align="center"><img src="https://raw.githubusercontent.com/akanz1/klib/main/examples/images/example_dist_plot.png" alt="Dist Plot Example" width="910" height="130"></p>\n\n```python\nklib.cat_plot(data, top=4, bottom=4) # representation of the 4 most & least common values in each categorical column\n```\n\n<p align="center"><img src="https://raw.githubusercontent.com/akanz1/klib/main/examples/images/example_cat_plot.png" alt="Cat Plot Example" width="1000" height="1000"></p>\n\nFurther examples, as well as applications of the functions in **klib.clean()** can be found <a href="https://github.com/akanz1/klib/tree/main/examples#data-cleaning-and-aggretation">here</a>.\n\n## Contributing\n\n[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/akanz1/klib)\n\nPull requests and ideas, especially for further functions are welcome. For major changes or feedback, please open an issue first to discuss what you would like to change.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Andreas Kanz',
    'author_email': 'andreas@akanz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.12',
}


setup(**setup_kwargs)
