<h1 align="center">Welcome to Python Panama REST API 👋</h1>
<p>
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/pythonpanama/python-panama-backend/blob/master/README.md">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" target="_blank" />
  </a>
  <a href="https://github.com/pythonpanama/python-panama-backend/graphs/commit-activity">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg" target="_blank" />
  </a>
  <a href="https://htmlpreview.github.io/?https://github.com/pythonpanama/python-panama-backend/blob/main/coverage_html_report/index.html">
    <img alt="Coverage" src="https://img.shields.io/badge/coverage-99%25-brightgreen.svg" target="_blank" />
  </a>  
  <a href="https://github.com/pythonpanama/python-panama-backend/blob/main/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" target="_blank" />
  </a>
  <a href="https://twitter.com/JavierFeliuA">
    <img alt="Twitter: JavierFeliuA" src="https://img.shields.io/twitter/follow/JavierFeliuA.svg?style=social" target="_blank" />
  </a>
</p>

## About
This project contains a REST API for performing CRUD operations on the Python 
Panama group's website [database](https://htmlpreview.github.io/?https://github.com/pythonpanama/python-panama-backend/blob/main/erd/erd.html). 

The project was built with Flask, using SQLAlchemy, Marshmallow, and JWT_Extended. For testing,
we used UnitTest.

## Install
To use the project in your development machine, clone it, and go to the project's root:
```sh
git clone https://github.com/pythonpanama/python-panama-backend.git
cd python-panama-backend
```
To run the development and the testing databases, go to the ```postgresql``` directory
and run ```docker-compose```:
```sh
cd postgresql
docker-compose up --build -d
```
Go back to the project's root:
```sh
cd ..
```
From the project's root, create and activate your virtual environment:
```sh
python3 -m venv venv
. venv/bin/activate
```
And install the project's dependencies:
```sh
pip install -r requirements.txt
```

## Development
Familiarize yourself with the codebase and modify as needed.  Important packages
and modules are:

- ```app.py``` Contains the Flask application factory.
- ```auth.py``` Uses flask_jwt_extended for fine-grained authentication/authorization.
- ```config.py``` Contains the configuration classes.
- ```models/``` Contains the SQLAlchemy models.
- ```resources/``` Contains the API resources and endpoints.
- ```schemas/``` Contains the Marshmallow schemas.
- ```tests/``` Contains the UnitTests.

Push your changes to the ```dev``` branch
```sh
git push origin dev
```
I will merge your changes with the ```main``` branch after reviewing them.

## Tests
To insure code quality, please add relevant tests for all production code additions/modifications.  

Make sure the virtual environment is activated before running the tests.

To run the tests use:
```sh
python -m unittest tests/**/*
```

If you wish to run the tests with coverage, use instead:
```sh
coverage run -m unittest tests/**/*
```
The included tests provide 99% coverage for the codebase.  You can find the coverage report [here](https://htmlpreview.github.io/?https://github.com/pythonpanama/python-panama-backend/blob/main/coverage_html_report/index.html).

## Mantainer

👤 **Javier Feliu**

* Twitter: [@JavierFeliuA](https://twitter.com/JavierFeliuA)
* Github: [@wanderindev](https://github.com/wanderindev)
* Email: [javier@wanderin.dev](mailto://javier@wanderin.dev)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

This project is [MIT](https://github.com/pythonpanama/python-panama-backend/blob/main/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
