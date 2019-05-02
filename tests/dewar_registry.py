import os
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

from tests import setup
from tests import labcontact
from tests import proposal

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

    facilityCodes = [ '{:0>4d}'.format(x) for x in range(30)]
    print(facilityCodes)

    session = setup.create_db_session()

    lc_params = {'card_name': 'LC1'}
    labcontact_id = labcontact.get_id(session, lc_params)
    proposal_id = proposal.get_id(session, "cm", "14451")

    if labcontact_id and proposal_id:
        for fc in facilityCodes:
            params = { "proposal_id": proposal_id,
                "labcontact_id": labcontact_id,
                "facility_code": "DLS-MX-{}".format(fc)}
            print("Adding facility code DLS-MX-{} to prop {}".format(fc, proposal_id))

            create(session, params)
    else:
        print("Error could not get proposal or labcontact id")
