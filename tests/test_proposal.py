import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

proposals = []

def create(session, params):
    """
    Create Proposal in db

    parameters:
      session - SQLAlchemy session object
      params - Dict containing proposal title, code and number
    """
    proposal = models.Proposal()
    proposal.title = params["title"]
    proposal.proposalCode = params["proposal_code"]
    proposal.proposalNumber = params["proposal_number"]
    # FK to person
    proposal.personId = params["person_id"]

    session.add(proposal)
    session.commit()

    # Add to our list of created proposals
    proposals.append(proposal.proposalId)

    return proposal.proposalId


def remove_all(session):
    """
    Remove test proposal and all related tables 
    using cascading delete in DB

    parameters:
      session - SQLAlchemy session object
      proposal_id - proposal id (primary key)
    """
    for id in proposals:        
        try:
            proposal = session.query(models.Proposal).get(id)
            session.delete(proposal)
            session.commit()
        except UnmappedInstanceError:
            print("Error - proposal not found {}".format(id))
        except IntegrityError:
            print("IntegrityError - can't remove proposal {}".format(id))

def get_id(session, proposal_code, proposal_number):
    prop = session.query(models.Proposal).filter(models.Proposal.proposalCode == proposal_code, models.Proposal.proposalNumber == proposal_number).one()
    return prop.proposalId
