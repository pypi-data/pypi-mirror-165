# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datapane',
 'datapane.client',
 'datapane.client.api',
 'datapane.client.api.report',
 'datapane.client.apps',
 'datapane.common',
 'datapane.resources',
 'datapane.resources.local_report',
 'datapane.resources.report_def',
 'datapane.resources.templates',
 'datapane.resources.templates.app',
 'datapane.resources.templates.hello',
 'datapane.resources.templates.report_py',
 'datapane.runner']

package_data = \
{'': ['*'], 'datapane.resources.templates': ['report_ipynb/*']}

install_requires = \
['Jinja2>=2.11.0,<3.1.0',
 'PyYAML>=6.0.0,<7.0.0',
 'altair>=4.0.0,<5.0.0',
 'boltons>=20.0.0,<22.0.0',
 'chardet>=3.0.4,<5.0.0',
 'click-spinner>=0.1.8,<0.2.0',
 'click>=7.1.0,<9.0.0',
 'colorlog>=4.1.0,<7.0.0',
 'dacite>=1.0.2,<2.0.0',
 'datacommons-pandas>=0.0.3,<0.0.4',
 'datacommons>=1.4.3,<2.0.0',
 'dominate>=2.4.0,<3.0.0',
 'dulwich>=0.20.45,<0.21.0',
 'furl>=2.0.0,<3.0.0',
 'glom>=20.5.0,<21.0.0',
 'importlib_resources>=3.0.0,<6.0.0',
 'jsonschema>=3.2.0,<5.0.0',
 'lxml>=4.0.0,<5.0.0',
 'micawber>=0.5.0',
 'munch>=2.3.0,<3.0.0',
 'nbconvert>=5.6.1,<7.0.0',
 'packaging>=20.0.0,<22.0.0',
 'pandas>=1.1.0,<2.0.0',
 'posthog>=1.4.0,<2.0.0',
 'pyarrow>=3.0.0,<7.0.0',
 'pydantic>=1.6.0,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.19.0,<3.0.0',
 'stringcase>=1.2.0,<2.0.0',
 'tabulate>=0.8.0,<0.9.0',
 'toolz>=0.11.0,<0.12.0',
 'validators>=0.18.0,<0.19.0',
 'vega-datasets>=0.9.0,<1.0.0']

extras_require = \
{'cloud': ['flit-core>=3.0.0,<3.1.0'],
 'plotting': ['matplotlib>=3.0.0,<4.0.0',
              'plotly>=4.0.0,<6.0.0',
              'bokeh>=2.4.2,<2.5.0',
              'folium>=0.12.0,<0.13.0',
              'plotapi>=5.0.0,<6.0.0']}

entry_points = \
{'console_scripts': ['datapane = datapane.client.__main__:main',
                     'dp-runner = datapane.runner.__main__:main']}

setup_kwargs = {
    'name': 'datapane',
    'version': '0.15.0',
    'description': 'Datapane client library and CLI tool',
    'long_description': '<p align="center">\n  <a href="https://datapane.com">\n    <img src="https://datapane.com/static/datapane-logo-dark.png" width="250px" alt="Datapane" />\n  </a>\n</p>\n<p align="center">\n  <a href="https://datapane.com">Datapane.com</a> |\n  <a href="https://docs.datapane.com">Docs</a> |\n      <a href="https://datapane.com/showcase">Examples</a> |\n  <a href="https://forum.datapane.com">Forums</a>   | <a href="https://chat.datapane.com">Discord</a>\n</p>\n<p align=\'center\'>\n  <a href="https://pypi.org/project/datapane/">\n      <img src="https://img.shields.io/pypi/dm/datapane?label=pip%20downloads" alt="Pip Downloads" />\n  </a>\n  <a href="https://pypi.org/project/datapane/">\n      <img src="https://img.shields.io/pypi/v/datapane?color=blue" alt="Latest release" />\n  </a>\n  <a href="https://anaconda.org/conda-forge/datapane">\n      <img alt="Conda (channel only)" src="https://img.shields.io/conda/vn/conda-forge/datapane">\n  </a>\n</p>\n\n<p align=\'center\'>\n  <h1 align=\'center\'> Build interactive reports in 3 lines of Python</h1>\n</p>\nDatapane is an open-source framework makes it easy to create beautiful reports from anywhere you can run Python.\nLove analyzing data in Python but struggle to share results and insights? Datapane is for you!\n<br>\n<br>\n<br>\n\n<p align="center">\n  <a href="https://datapane.com">\n    <img src="https://user-images.githubusercontent.com/3541695/176545400-919a327d-ddee-4755-b29f-bf85fbfdb4ef.png"  width=\'75%\'>\n  </a>\n</p>\n\n### What makes Datapane special?\n\n-   **Static generation:** Sharing a report shouldn\'t require deploying an app. Render a standalone HTML bundle which you can share or host on the web.\n-   **API-first and programmatic:** Programmatically generate reports from inside of Spark, Airflow, or Jupyter. Schedule updates to build real-time dashboards.\n-   **Dynamic front-end components**: Say goodbye to writing HTML. Build reports from a set of interactive components, like DataTables, tabs, and selects.\n\n# Getting Started\n\nWant a head start? Check out our _Datapane in 3 minutes_ video:\n\nhttps://user-images.githubusercontent.com/15690380/179759362-e577a4f8-d1b7-4b8d-9190-0c13d5015728.mp4\n\n## Installing Datapane\n\nThe best way to install Datapane is through pip or conda.\n\n#### pip\n\n```\n$ pip3 install -U datapane\n```\n\n#### conda\n\n```\n$ conda install -c conda-forge "datapane>=0.14.0"\n```\n\nDatapane also works well in hosted Jupyter environments such as Colab or Binder, where you can install as follows:\n\n```\n!pip3 install --quiet datapane\n```\n\n# Creating reports\n\n### 📊 Include plots and data\n\nCreate a report from pandas DataFrames, plots from your favorite libraries, and text.\n\n<p>\n\n<img width=\'485px\' align=\'left\' alt="Simple Datapane report example with text, plot and table" src="https://user-images.githubusercontent.com/3541695/176251650-f49ea9f8-3cd4-4eda-8e78-ccba77e8e02f.png">\n\n<p>\n\n```python\nimport altair as alt\nfrom vega_datasets import data\nimport datapane as dp\n\ndf = data.iris()\nfig = (\n    alt.Chart(df)\n    .mark_point()\n    .encode(\n      x="petalLength:Q",\n      y="petalWidth:Q",\n      color="species:N"\n    )\n)\nreport = dp.Report(\n    dp.Plot(fig),\n    dp.DataTable(df)\n)\nreport.save(path="my_report.html")\n```\n\n</p>\n\n### 🎛 Layout using interactive blocks\n\nAdd dropdowns, selects, grid, pages, and 10+ other blocks to make your reports dynamic.\n\n<p>\n\n<img width=\'485px\' align=\'left\' alt="Complex layout" src="https://user-images.githubusercontent.com/3541695/176288321-44f7e76f-5032-434b-a3b0-ed7e3911b5d5.png">\n\n<p >\n\n```python\n\n\n...\n\ndp.Report(\n    dp.Formula("x^2 + y^2 = z^2"),\n    dp.Group(\n        dp.BigNumber(\n            heading="Number of percentage points",\n            value="84%",\n            change="2%",\n            is_upward_change=True\n        ),\n        dp.BigNumber(\n            heading="Simple Statistic", value=100\n        ), columns=2\n    ),\n    dp.Select(\n        dp.Plot(fig, label="Chart"),\n        dp.DataTable(df, label="Data")\n    ),\n).save(path="Layout_example.html")\n\n```\n\n</p>\n</p>\n\n<br>\n<br>\n<br>\n\n# Get involved\n\n## Discord\n\nOur Discord community is for people who believe that insights, visualizations, and reports are better created with Python instead of drag-and-drop tools. Get help from the team, share what you\'re building, and get to know others in the space!\n\n### 💬 [Join our discord server](https://chat.datapane.com)\n\n## Forums\n\nGot feature requests, feedback, or questions? Visit our Forum.\n\n### 📮 [Join our forum](https://forum.datapane.com/)\n\n# Hosting Reports\n\nIn addition to saving documents locally or hosting them yourself, you can host and share your reports using [Datapane Cloud](https://datapane.com/cloud).\n\nTo get your API key, [create a free account](https://datapane.com/accounts/signup/).\n\nNext, in your Python notebook or script, change the `save` function to `upload`:\n\n```python\ndp.Report(\n ...\n#).save(path="hello_world.html")\n).upload(name="Hello world")\n```\n\n# Demos and Examples\n\nHere a few samples of the top reports created by the Datapane community.\n\n-   [Coindesk analysis](https://datapane.com/u/greg/reports/initial-coindesk-article-data/) by Greg Allan\n-   [COVID-19 Trends by Quarter](https://datapane.com/u/keith8/reports/covid-19-trends-by-quarter/) by Keith Johnson\n-   [Ecommerce Report](https://datapane.com/u/leo/reports/e-commerce-report/) by Leo Anthias\n-   [Example Academic Paper](https://datapane.com/u/kalru/reports/supplementary-material/) by Kalvyn Roux\n-   [Exploration of Restaurants in Kyoto](https://datapane.com/u/ryancahildebrandt/reports/kyoto-in-stations-and-restaurants/) by Ryan Hildebrandt\n\n# Next Steps\n\n-   [Join Discord](https://chat.datapane.com)\n-   [Sign up for a free account](https://datapane.com/accounts/signup)\n-   [Read the documentation](https://docs.datapane.com)\n\n## Analytics\n\nBy default, the Datapane Python library collects error reports and usage telemetry.\nThis is used by us to help make the product better and to fix bugs.\nIf you would like to disable this, simply create a file called `no_analytics` in your `datapane` config directory, e.g.\n\n### Linux\n\n```bash\n$ mkdir -p ~/.config/datapane && touch ~/.config/datapane/no_analytics\n```\n\n### macOS\n\n```bash\n$ mkdir -p ~/Library/Application\\ Data/datapane && touch ~/Library/Application\\ Data/no_analytics\n```\n\n### Windows (PowerShell)\n\n```powershell\nPS> mkdir ~/AppData/Roaming/datapane -ea 0\nPS> ni ~/AppData/Roaming/datapane/no_analytics -ea 0\n```\n\nYou may need to try `~/AppData/Local` instead of `~/AppData/Roaming` on certain Windows configurations depending on the type of your user-account.\n',
    'author': 'Datapane Team',
    'author_email': 'dev@datapane.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.datapane.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11.0',
}


setup(**setup_kwargs)
