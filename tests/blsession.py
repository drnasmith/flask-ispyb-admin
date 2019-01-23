import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

def create(session, params):
    """
    Create BLSession in db

    parameters:
      session - SQLAlchemy session object
      params - Dict containing session info and proposal FK
    """
    blsession = models.BLSession()
    blsession.sessionTitle = params["session_title"]
    blsession.beamLineName = params["beamline_name"]
    blsession.visit_number = params["visit_number"]
    # Default start date of now and end date +5 days
    blsession.startDate = datetime.datetime.now()
    blsession.endDate = blsession.startDate + datetime.timedelta(days=5)
    # FK to person
    blsession.proposalId = params["proposal_id"]

    session.add(blsession)
    session.commit()

    return blsession.sessionId


def add_person(session, params):
    """
    Function to associate a person to a session 
    - required for logging in via synchweb

    parameters:
      session - SQLAlchemy session object
      params - Dict containing person and session FKs
    """
    session_has_person = models.SessionHasPerson()
    session_has_person.personId = params["person_id"]
    session_has_person.sessionId = params["bl_session_id"]

    session.add(session_has_person)
    session.commit()


