# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['azpypkg36']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'azpypkg36',
    'version': '0.1.0',
    'description': 'AaronZ Learning Python Package',
    'long_description': '\n# AZPyPkg\n\nAZ Learning Package\n\n\n## Set up\n1. Install envrionment manager: Anaconda(Or even smaller package of Miniconda)\n2. Install packages: `poetry` and `cookiecutter`\n3. Register for TestPyPI and PyPI \n4. Register for GitHub\n5. Install Python extensions in VSCode\n\n\n\n## Main\n1. Create a new virtual env by Anaconda and make it enable in VSCode to working directory locally\n2. Create a new package structure by below command and input a few info. `git init` the new folder \n\n    `cookiecutter https://github.com/py-pkgs/py-pkgs-cookiecutter.git`\n\n    ![](Pic/1.png)\n3. Create a new project in GitHub, link new package to remote repos. Commit and push:\n\n    ![](Pic/2.png)\n\n    ![](Pic/3.png)\n4. Add new code as function into file \'azpypkg36\': \n\n    ![](Pic/4.png)\n5. Install current new package: `poetry install`\n\n    ![](Pic/5.png)\n\n    ![](Pic/6.png)\n6. Test new installed package:\n\n   Create test file \'zen.txt\': `python -c "import this" > zen.txt`\n\n   ![](Pic/7.png)\n\n   Test with Python Command:\n\n   ![](Pic/8.png) \n\n   Test with tests .py file:\n\n   ![](Pic/9.png)\n\n8. Create tests in \'tests\' directory and run test: `pytest tests/`\n    Install \'pytest\' into project: `poetry add --dev pytest`\n\n    ![](Pic/12.png)\n\n    Create unit test code: **KEY**: both file name and function name, must include \'test_XXX\' or \'XXX_test\'\n\n    ![](Pic/10.png)\n\n    Run unit test:\n\n    ![](Pic/11.png)\n    \n9. Check code coverage:\n\n    Install \'pytest\' into project: `poetry add --dev pytest-cov`\n\n    ![](Pic/13.png)\n\n    Run test coverage: `pytest tests/ --cov=azpypkg36`\n\n    ![](Pic/14.png)\n\n10. Documentation:\n\n    ([TBSummary](https://py-pkgs.org/03-how-to-package-a-python#package-documentation))\n\n11. Add version:\n\n    `git tag` + `git push --tags` after regular `git commit` and `git push`\n\n    ![](Pic/15.png)\n\n12. Release on github:\n\n    ![](Pic/16.png)\n    ![](Pic/17.png)\n    ![](Pic/18.png)\n\n13. Build package: the main reason for build is to generate a a wheel(.whl file) can be distributed\n\n    \n14. Install locally:\n15. Publish package:\n    1.  Publish to \'TestPyPI\':\n    2.  Publish to \'PyPI\':\n\n\n\n## More details steps:',
    'author': 'AaronZ',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
