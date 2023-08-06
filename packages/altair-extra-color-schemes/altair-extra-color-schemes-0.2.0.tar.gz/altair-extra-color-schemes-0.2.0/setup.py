# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['altair_extra_color_schemes']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.2,<4.3']

entry_points = \
{'altair.vegalite.v4.renderer': ['extra_color_schemes = '
                                 'altair_extra_color_schemes.renderer:extra_color_schemes_renderer']}

setup_kwargs = {
    'name': 'altair-extra-color-schemes',
    'version': '0.2.0',
    'description': 'Additional named color schemes for Altair via a custom renderer.',
    'long_description': '# altair-extra-color-schemes\n\nAdditional named color schemes for [Altair](https://altair-viz.github.io/) via a custom renderer.\n\n## Quickstart\n\n### Installation\n\nVia [pip](https://pip.pypa.io/):\n\n```bash\npip install altair-extra-color-schemes\n```\n\nVia [Pipenv](https://pipenv.pypa.io/):\n\n```bash\npipenv install altair-extra-color-schemes\n```\n\nVia [Poetry](https://python-poetry.org/):\n\n```bash\npoetry add altair-extra-color-schemes\n```\n\nVia [PDM](https://pdm.fming.dev/):\n\n```bash\npdm add altair-extra-color-schemes\n```\n\nVia [Pyflow](https://github.com/David-OConnor/pyflow):\n\n```bash\npyflow install altair-extra-color-schemes\n```\n\n### Usage\n\n```python\nimport altair as alt\nalt.renderers.enable("extra_color_schemes")\n```\n\nYou can find some example charts in the [`demo.ipynb` notebook](demo.ipynb).\n\n## Color schemes\n\n| Color scheme name | [Type](https://vega.github.io/vega/docs/schemes/) | Source                                                                                                | Notes                                                          |\n| ----------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |\n| `"dvs"`           | Categorical                                       | [Data Visualization Standards (DVS)](https://xdgov.github.io/data-design-standards/components/colors) | "Featured Colors" and "Qualitative Colors" > "Example Palette" |\n\n## Development\n\n<!-- > [Poetry](https://python-poetry.org/) (version 1.2.0b3) -->\n\n> [Poetry](https://python-poetry.org/) (version 1.2.0)\n\nAdd new color schemes to the `altair_extra_color_schemes/full_template.jinja` file\n\n- `poetry config virtualenvs.in-project true`\n- `poetry install`\n- `poetry run jupyter lab`\n- `poetry run black demo.ipynb`\n- `poetry check`\n\n## Deployment\n\n- `poetry version minor` or `poetry version patch`\n- `poetry build`\n\n## Notes\n\n- [djLint](https://djlint.com/):\n  - `pipx install djlint`\n  - `djlint altair_extra_color_schemes/template.jinja --check`\n  - `djlint altair_extra_color_schemes/template.jinja --reformat`\n  - `djlint altair_extra_color_schemes/template.jinja --profile=jinja`\n  - `djlint formatter.jinja --reformat --format-css --format-js`\n- [Default color schemes](https://vega.github.io/vega-lite/docs/scale.html#scheme)\n- [DjHTML](https://github.com/rtts/djhtml):\n  - `pipx install djhtml`\n  - `djhtml -i formatter.html`\n- [curlylint](https://www.curlylint.org/):\n  - `pipx install curlylint`\n  - `curlylint altair_extra_color_schemes/full_template.jinja`\n- [Cloudscape Design System](https://www.figma.com/community/file/1130789169293366599) (Figma file)\n- Poetry:\n  - [Detection of the currently active Python (experimental)](https://python-poetry.org/blog/announcing-poetry-1.2.0/#detection-of-the-currently-active-python-experimental) documentation\n  - [Can\'t install Pandas on Mac M1](https://github.com/pandas-dev/pandas/issues/40611) issue\n- `pip --version`\n- [Nullish coalescing operator (??): Short-circuiting](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing_operator#short-circuiting)\n',
    'author': 'João Palmeiro',
    'author_email': 'joaopalmeiro@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/joaopalmeiro/altair-extra-color-schemes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
