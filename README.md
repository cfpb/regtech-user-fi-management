# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-user-fi-management/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                   |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|----------------------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/regtech\_user\_fi\_management/config.py                            |       33 |        0 |        2 |        1 |     97% |    16->20 |
| src/regtech\_user\_fi\_management/dependencies.py                      |       15 |        0 |        4 |        0 |    100% |           |
| src/regtech\_user\_fi\_management/entities/engine/engine.py            |       10 |        0 |        0 |        0 |    100% |           |
| src/regtech\_user\_fi\_management/entities/listeners.py                |       55 |        5 |       24 |        4 |     89% |18->13, 26->13, 40->33, 51->exit, 71-77 |
| src/regtech\_user\_fi\_management/entities/models/dao.py               |       85 |        0 |        2 |        0 |    100% |           |
| src/regtech\_user\_fi\_management/entities/models/dto.py               |      115 |        0 |       12 |        1 |     99% |    89->93 |
| src/regtech\_user\_fi\_management/entities/repos/institutions\_repo.py |       54 |        0 |       12 |        1 |     98% |    68->72 |
| src/regtech\_user\_fi\_management/entities/repos/repo\_utils.py        |        6 |        0 |        0 |        0 |    100% |           |
| src/regtech\_user\_fi\_management/main.py                              |       43 |       11 |        0 |        0 |     74% |32-36, 41-46 |
| src/regtech\_user\_fi\_management/routers/\_\_init\_\_.py              |        3 |        0 |        0 |        0 |    100% |           |
| src/regtech\_user\_fi\_management/routers/admin.py                     |       27 |        0 |        2 |        0 |    100% |           |
| src/regtech\_user\_fi\_management/routers/institutions.py              |       87 |        0 |       18 |        3 |     97% |94->exit, 137->exit, 160->exit |
|                                                              **TOTAL** |  **533** |   **16** |   **76** |   **10** | **96%** |           |

6 empty files skipped.


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/cfpb/regtech-user-fi-management/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-user-fi-management/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cfpb/regtech-user-fi-management/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-user-fi-management/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fcfpb%2Fregtech-user-fi-management%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/cfpb/regtech-user-fi-management/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.