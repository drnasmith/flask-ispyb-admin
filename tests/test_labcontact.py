import os
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

labcontacts = []

def create(session, params):
    """
    Create Labcontact in db

    parameters:
      session - SQLAlchemy session object
      params - Dict containing user info login
    """
    labcontact = models.LabContact()
    labcontact.cardName = params["card_name"]
    labcontact.defaultCourrierCompany = "DHL"
    labcontact.courierAccount = "1234567890"
    labcontact.dewarAvgCustomsValue = "100"
    labcontact.recordTimeStamp = datetime.datetime.now()
    
    # Find person
    person = session.query(models.Person).get(params['person_id'])
    proposal = session.query(models.Proposal).get(params['proposal_id'])

    labcontact.personId = person.personId
    labcontact.proposalId = proposal.proposalId

    try:
        session.add(labcontact)
        session.commit()

        # Add created labcontact to our list of generated lab contacts
        # Deleting the proposal should delete this labcontact
        labcontacts.append(labcontact.labContactId)
    except IntegrityError:
        session.rollback()
        print("labcontact {} already exists..".format(params["card_name"]))

        # labcontact already exists, try to get the existing one
        # Note we don't add this to our list of created labcontacts
        labcontact = (
            session.query(models.Labcontact)
            .filter(models.Labcontact.cardName == params["card_name"])
            .one()
        )

    return labcontact.labContactId


def get_id(session, params):
    """
    Get the Labcontact specified by params (card_name)

    Parameters:
      params - dictionary of params obj
    """
    query = session.query(models.LabContact).filter(models.LabContact.cardName == params["card_name"])
    labcontact = query.one()

    return labcontact.labContactId


