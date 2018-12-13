import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

from tests import test_person
from tests import test_proposal
from tests import test_datacollection
from tests import test_blsession
from tests import test_shipping
from tests import test_dewars
from tests import test_labcontact

def create_db_session():
    """
    Generate a SQLAlchemy session object
    """
    conn = "mysql+mysqlconnector://ispyb:integration@192.168.33.11:3306/ispyb"
    engine = create_engine(conn)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def create_all():
    proposal_code = 'cm'
    proposal_number = '1001'

    session = create_db_session()

    # Try to create new test user
    person = {"login": "jbloggs", "given_name": "Joe", "family_name": "Bloggs"}
    person_id = test_person.create(session, person)

    # Create Proposal
    proposal = {
        "title": "Test Proposal {}{}".format(proposal_code, proposal_number),
        "proposal_code": proposal_code,
        "proposal_number": proposal_number,
        "person_id": person_id,
    }

    proposal_id = test_proposal.create(session, proposal)
    print("Proposal id = {}".format(proposal_id))

    # Create Session
    blsession = {
        "session_title": "Auto-generated session",
        "visit_number": "1",
        "beamline_name": "i02",
        "proposal_id": proposal_id,
    }
    bl_session_id = test_blsession.create(session, blsession)
    print("Session id = {}".format(bl_session_id))

    # Associate Session with User
    shp_params = {"person_id": person_id, "bl_session_id": bl_session_id}
    test_blsession.add_person(session, shp_params)

    #
    # Shipment
    #
    # Create a labcontact first
    labcontact_params = {
        'card_name': 'Lab contact {}'.format(''.join([proposal_code, proposal_number])),
        'person_id': person_id,
        'proposal_id': proposal_id
    }
    labcontact_id = test_labcontact.create(session, labcontact_params)

    shipment_params = { 'shipping_name': 'Auto-generated shipment', 'proposal_id' : proposal_id, 'labcontact_id': labcontact_id}
    shipment_id = test_shipping.create(session, shipment_params)

    dewars = []
    for i in range(5):
        dewar_params = {}
        dewar_params['facility_code'] = "DLS-CM-000{}".format(i)
        dewar_params['barcode'] = "cm1001-i02-000{}".format(i)
        dewar_params['storage_location'] = "EBIC-IN-{}".format(i)
        dewar_params['dewar_status'] = "at facility"
        dewar_params['barcode'] = "cm1001-i02-000{}".format(i)
        dewar_params['shipping_id'] = shipment_id

        dewar_id = test_dewars.create(session, dewar_params)

        dewars.append(dewar_id)

    # Add Dewar Transport History for first couple
    for index, dewar in enumerate(dewars[0:2]):
        dewar_params = {}
        dewar_params['storage_location'] = 'EBIC-OUT-{}'.format(index)
        dewar_params['dewar_status'] = 'at-facility'
        dewar_params['dewar_id'] = dewar

        test_dewars.add_history(session, dewar_params)
        
    # # Add Data collection to session
    # # First create data collection group
    # dc_params = {"bl_session_id": bl_session_id}
    # dcg_id = test_datacollection.create_data_collection_group(session, dc_params)

    # # Next create the actual data collection
    # dc_params["data_collection_group_id"] = dcg_id
    # test_datacollection.create_data_collection(session, dc_params)

    # Return proposal id as we need this to delete test data
    return proposal_id



def remove_all():
    """
    Remove test proposal and all related tables 
    using cascading delete in DB
    """
    session = create_db_session()

    # Remove data collection groups and collections (no cascade here...)
    test_datacollection.remove_all(session)

    # Remove proposal which will remove sessions, shipments etc
    test_proposal.remove_all(session)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", default=True, help="Create db tables")
    parser.add_argument("-r", "--remove", action="store_true", default=False, help="Tidy afterwards - remove created tables")

    args = parser.parse_args()

    if args.create:
        print("Create DB tables")
        proposal_id = create_all()
        print("Created Tables for Proposal Id: {}".format(proposal_id))

    if args.remove:
        print("Remove DB tables..")
        remove_all()
 
