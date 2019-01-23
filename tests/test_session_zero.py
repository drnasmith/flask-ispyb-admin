import os
import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

from tests import person
from tests import proposal
from tests import blsession

from tests.db import create_db_session

def create_all():
    proposal_code = 'cm'
    proposal_number = '1001'

    session = create_db_session()

    # Try to create new test user (for logging in to cas)
    person_params = {"login": "boaty", "given_name": "Boaty", "family_name": "McBoatface"}
    person_id = person.create(session, person_params)

    # Create Proposal
    proposal_params = {
        "title": "Auto Generated Test Proposal {}{}".format(proposal_code, proposal_number),
        "proposal_code": proposal_code,
        "proposal_number": proposal_number,
        "person_id": person_id,
    }

    proposal_id = proposal.create(session, proposal_params)
    print("Proposal id = {}".format(proposal_id))

    # Create Session 0
    blsession_params = {
        "session_title": "Auto-generated session",
        "visit_number": "0",
        "beamline_name": "i02",
        "proposal_id": proposal_id,
    }
    bl_session_id = blsession.create(session, blsession_params)
    print("Session id = {}".format(bl_session_id))

    shp_params = {"person_id": person_id, "bl_session_id": bl_session_id}
    blsession.add_person(session, shp_params)

    # # Create Session 1
    # blsession_params = {
    #     "session_title": "Auto-generated session",
    #     "visit_number": "1",
    #     "beamline_name": "i02",
    #     "proposal_id": proposal_id,
    # }
    # bl_session_id = blsession.create(session, blsession_params)
    # print("Session id = {}".format(bl_session_id))

    # shp_params = {"person_id": person_id, "bl_session_id": bl_session_id}
    # blsession.add_person(session, shp_params)

def remove_all():
    """
    Remove test proposal and all related tables 
    using cascading delete in DB
    """
    session = create_db_session()

    # Remove proposal which will remove sessions, shipments etc
    proposal.remove_all(session)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", default=False, help="Create db tables")
    parser.add_argument("-r", "--remove", action="store_true", default=False, help="Tidy afterwards - remove created tables")

    args = parser.parse_args()

    if args.create:
        print("Create DB tables")
        create_all()

    if args.remove:
        print("Remove DB tables..")
        remove_all()
 
