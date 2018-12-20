import os
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

from tests import setup
from tests import test_labcontact
from tests import test_proposal

def create(session, params):
    """
    Create Dewar in db

    parameters:
      session - SQLAlchemy session object
      params - Dict containing dewar info and shipping FK
    """
    dewar = models.DewarRegistry()
    dewar.proposalId = params["proposal_id"]
    dewar.labContactId = params["labcontact_id"]
    dewar.facilityCode = params["facility_code"]
    dewar.purchaseDate = datetime.datetime.now()

    session.add(dewar)
    session.commit()

    return dewar.facilityCode

if __name__ == "__main__":

    session = setup.create_db_session()

    lc_params = {'card_name': 'Blah'}
    labcontact_id = test_labcontact.get_id(session, lc_params)
    proposal_id = test_proposal.get_id(session, "cm", "1001")

    if labcontact_id and proposal_id:
        params = { "proposal_id": proposal_id,
            "labcontact_id": labcontact_id,
            "facility_code": "DLS-MX-1001"}

        create(session, params)
    else:
        print("Error could not get proposal or labcontact id")