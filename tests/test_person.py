import os
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

persons = []

def create(session, params):
    """
    Create Person in db

    parameters:
      session - SQLAlchemy session object
      params - Dict containing user info login
    """
    person = models.Person()
    person.login = params["login"]
    person.givenName = params["given_name"]
    person.familyName = params["family_name"]

    try:
        session.add(person)
        session.commit()

        # Add created person to our list of generated people
        persons.append(person.personId)
    except IntegrityError:
        session.rollback()
        print("Person {} already exists..".format(params["login"]))

        # Person already exists, try to get the existing one
        # Note we don't add this to our list of created persons
        person = (
            session.query(models.Person)
            .filter(models.Person.login == params["login"])
            .one()
        )

    return person.personId


def get_id(session, params):
    """
    Get the Person specified by params (login or first/surname)

    Parameters:
      params - dictionary of params obj
    """
    query = session.query(models.Person)

    if params["login"]:
        query = query.filter(models.Person.login == params["login"])

    elif params["first_name"] and params["family_name"]:
        query = query.filter(models.Person.givenName == params["given_name"])
        query = query.filter(models.Person.familyName == params["family_name"])

    person = query.one()

    return person.personId


