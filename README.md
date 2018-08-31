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
Edit config module to reflect credentials

$ python app.py

http://localhost:9000/admin 

## Security
This is not a secure app and is only intended to run on development systems.
There is a basic auth included - edit credentials in the app (or get from env vars)


