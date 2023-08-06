# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_markdown_docs']

package_data = \
{'': ['*']}

install_requires = \
['markdown-it-py>=1.1.0,<1.2.0']

entry_points = \
{'pytest11': ['pytest_markdown_docs = pytest_markdown_docs.plugin']}

setup_kwargs = {
    'name': 'pytest-markdown-docs',
    'version': '0.4.1',
    'description': 'Run markdown code fences through pytest',
    'long_description': '# Pytest Markdown Docs\n\nA plugin for [pytest](https://docs.pytest.org) that uses markdown code snippets from markdown files and docstrings as tests.\n\nDetects Python code fences (triple backtick escaped blocks) in markdown files as\nwell as inline Python docstrings (similar to doctests) and runs them as tests.\n\nPython file example:\n\n````python\n# mymodule.py\nclass Foo:\n    def bar(self):\n        """Bar the foo\n\n        This is a sample docstring for the bar method\n\n        Usage:\n        ```python\n        import mymodule\n        result = mymodule.Foo().bar()\n        assert result == "hello"\n        ```\n        """\n        return "hello"\n````\n\nMarkdown file examples:\n\n````markdown\n# Title\n\nLorem ipsum yada yada yada\n\n```python\nimport mymodule\nresult = mymodule.Foo().bar()\nassert result == "hello"\n```\n````\n\n## Usage\n\nFirst, make sure to install the plugin, e.g. `pip install pytest-markdown-docs`\n\nTo enable markdown python tests, pass the `--markdown-docs` flag to `pytest`:\n```shell\npytest --markdown-docs\n```\n\nYou can also use the `markdown-docs` flag to filter *only* markdown-docs tests:\n```shell\npytest --markdown-docs -m markdown-docs\n```\n\n### Detection conditions\n\nFence blocks (` ``` `) starting with the `python`, `python3` or `py` language definitions are detected as tests in:\n\n* Python (.py) files, within docstrings of classes and functions\n* `.md`, `.mdx` and `.svx` files\n\n## Skipping tests\n\nTo exclude a Python code fence from testing, add a `notest` info string to the\ncode fence, e.g:\n\n````markdown\n```python notest\nprint("this will not be run")\n```\n````\n\n## Code block dependencies\n\nSometimes you might wish to run code blocks that depend on entities to already\nbe declared in the scope of the code, without explicitly declaring them. There\nare currently two ways you can do this with pytest-markdown:\n\n### Injecting global/local variables\n\nIf you have some common imports or other common variables that you want to make\nuse of in snippets, you can add them by creating a `pytest_markdown_docs_globals`\nhook in your `conftest.py`:\n\n```python\ndef pytest_markdown_docs_globals():\n    import math\n    return {"math": math, "myvar": "hello"}\n```\n\nWith this conftest, you would be able to run the following markdown snippet as a\ntest, without causing an error:\n\n````markdown\n```python\nprint(myvar, math.pi)\n```\n````\n\n### Fixtures\n\nYou can use both `autouse=True` pytest fixtures in a conftest.py or named fixtures with\nyour markdown tests. To specify named fixtures, add `fixture:<name>` markers to the code\nfence info string, e.g.,\n\n````markdown\n```python fixture:capsys\nprint("hello")\ncaptured = capsys.readouterr()\nassert captured.out == "hello\\n"\n```\n````\nAs you can see above, the fixture value will be injected as a global. For `autouse=True` fixtures, the value is only injected as a global if it\'s explicitly added using a `fixture:<name>` marker.\n\n\n### Depending on previous snippets\n\nIf you have multiple snippets following each other and want to keep the side\neffects from the previous snippets, you can do so by adding the `continuation`\ninfo string to your code fence:\n\n````markdown\n```python\na = "hello"\n```\n\n```python continuation\nassert a + " world" == "hello world"\n```\n````\n\n## Testing of this plugin\nYou can test this module itself (sadly not using markdown tests at the moment) using pytest:\n\n```shell\n> poetry run pytest\n```\n\nOr for fun, you can use this plugin to include testing of the validity of snippets in this README.md file:\n```shell\n> poetry run pytest --markdown-docs\n```\n\n\n## Known issues\n* Only tested with pytest 6.2.5. There seem to be some minor issue with pytest >7 due to changes of some internal functions in pytest, but that should be relatively easy to fix. Contributions are welcome :)\n* Code for docstring-inlined test discovery can probably be done better (similar to how doctest does it). Currently, seems to sometimes traverse into Python\'s standard library which isn\'t great...\n* Traceback logic is extremely hacky, wouldn\'t be surprised if the tracebacks look weird sometimes\n    - Line numbers are "wrong" for docstring-inlined snippets (since we don\'t know where in the file the docstring starts)\n    - Line numbers are "wrong" for continuation blocks even in pure markdown files (can be worked out with some refactoring)\n',
    'author': 'Modal Labs',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/modal-com/pytest-markdown-docs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
