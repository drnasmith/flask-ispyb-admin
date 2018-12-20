import os
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

laboratories = []

def create(session, params):
    """
    Create Labcontact in db

    parameters:
      session - SQLAlchemy session object
      params - Dict containing user info login
    """
    laboratory = models.Laboratory()
    laboratory.name = params["name"]
    laboratory.address = params["address"]
    laboratory.city = params["city"]
    laboratory.postcode = params["post_code"]
    laboratory.recordTimeStamp = datetime.datetime.now()
    
    try:
        session.add(laboratory)
        session.commit()

        # Add created laboratory to our list of generated lab contacts
        # We will need to delete this ourselves as it has no Fks to Proposal
        laboratories.append(laboratory.laboratoryId)
    except IntegrityError:
        session.rollback()
        print("laboratory {} already exists..".format(params["name"]))

        # laboratory already exists, try to get the existing one
        # Note we don't add this to our list of created laboratorys
        laboratory = (
            session.query(models.laboratory)
            .filter(models.laboratory.cardName == params["name"])
            .one()
        )

    return laboratory.laboratoryId


def get_id(session, params):
    """
    Get the laboratory specified by params (card_name)

    Parameters:
      params - dictionary of params obj
    """
    query = session.query(models.Laboratory).filter(models.Laboratory.name == params["name"])
    laboratory = query.one()

    return laboratory.laboratoryId


