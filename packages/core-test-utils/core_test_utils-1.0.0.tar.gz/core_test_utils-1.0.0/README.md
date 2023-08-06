# test-utils

**Using**

1. `python -m pip install core_test_utils`


**Buidling**

1. Increase the version in `setup.cfg` file

2. Create a file ~/.pypirc in root directory of your system and paste below data in the file.

        [distutils]
        index-servers =
                local

        [local]
        repository = https://upload.pypi.org/legacy/
 
4. After making changes in the test_utils go to source directory of code and run below command to build the wheel and push to artifactory

        - python3 -m pip install --upgrade build
        - python3 -m build
        - python3 -m pip install --upgrade twine
        - python3 -m twine upload --repository local --verbose dist/*
        - Enter the username and password of your pypi account
 
5. That's all you have to do and now you are good to use the core_test_utils in your project
  
