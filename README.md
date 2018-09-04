# Project to administer test ISPyB databases

## Setup

Create a virtual environment and use pip to install dependencies
$ pip install -r requirements.txt

This should install:
 - flask
 - SQLAlchemy
 - MySQL-Python (for python < 3)
If on python < 3.4 than also 
 - enum34

## Running
Create/edit config.py module to reflect credentials (see ispyb/__init__.py for format)

`python app.py`

View in browser, http://localhost:9000/admin 

## Security
This is not a secure app and is only intended to run on development systems.
There is a basic auth included - credentials are generated on startup (check console)


# Setup/Update models
To recreate the database models you can use sqlacodegen

## Install sqlacodegen
`pip install 'sqlacodegen <= 2.0.0'`

(Version 2.0.0 upwards has issues with VARCHAR length)

## Generate models
`sqlacodegen mysql://<user>:<password>@<host>/<db_name> --outfile gen_models.py`

Then compare the generated models with ispyb/models.py

Some changes are required to fit the models file into flask SQLAlchemy conventions.

From newly generated file:

Changes to models.py:
- `- from sqlalchemy.ext.declarative import declarative_base`
- `- Base = declarative_base()` 
- `- metadata = Base.metadata`
- `+ from . import Base`
- replace `metadata with Base.metadata`

## Check model list is consistent
`grep '(Base)' gen_models.py | sed s'/class //' | sed s'/(Base)://'`

Add these to a model_list.py file within ispyb directory (replace existing one)
