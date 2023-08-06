
# AZPyPkg

AZ Learning Package


## Set up
1. Install envrionment manager: Anaconda(Or even smaller package of Miniconda)
2. Install packages: `poetry` and `cookiecutter`
3. Register for TestPyPI and PyPI 
4. Register for GitHub
5. Install Python extensions in VSCode



## Main
1. Create a new virtual env by Anaconda and make it enable in VSCode to working directory locally
2. Create a new package structure by below command and input a few info. `git init` the new folder 

    `cookiecutter https://github.com/py-pkgs/py-pkgs-cookiecutter.git`

    ![](Pic/1.png)
3. Create a new project in GitHub, link new package to remote repos. Commit and push:

    ![](Pic/2.png)

    ![](Pic/3.png)
4. Add new code as function into file 'azpypkg36': 

    ![](Pic/4.png)
5. Install current new package: `poetry install`

    ![](Pic/5.png)

    ![](Pic/6.png)
6. Test new installed package:

   Create test file 'zen.txt': `python -c "import this" > zen.txt`

   ![](Pic/7.png)

   Test with Python Command:

   ![](Pic/8.png) 

   Test with tests .py file:

   ![](Pic/9.png)

8. Create tests in 'tests' directory and run test: `pytest tests/`
    Install 'pytest' into project: `poetry add --dev pytest`

    ![](Pic/12.png)

    Create unit test code: **KEY**: both file name and function name, must include 'test_XXX' or 'XXX_test'

    ![](Pic/10.png)

    Run unit test:

    ![](Pic/11.png)
    
9. Check code coverage:

    Install 'pytest' into project: `poetry add --dev pytest-cov`

    ![](Pic/13.png)

    Run test coverage: `pytest tests/ --cov=azpypkg36`

    ![](Pic/14.png)

10. Documentation:

    ([TBSummary](https://py-pkgs.org/03-how-to-package-a-python#package-documentation))

11. Add version:

    `git tag` + `git push --tags` after regular `git commit` and `git push`

    ![](Pic/15.png)

12. Release on github:

    ![](Pic/16.png)
    ![](Pic/17.png)
    ![](Pic/18.png)

13. Build package: the main reason for build is to generate a a wheel(.whl file) can be distributed

    
14. Install locally:
15. Publish package:
    1.  Publish to 'TestPyPI':
    2.  Publish to 'PyPI':



## More details steps: