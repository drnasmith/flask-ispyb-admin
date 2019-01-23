import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

from tests import person
from tests import proposal
from tests import datacollection
from tests import blsession
from tests import shipping
from tests import dewars
from tests import labcontact
from tests import laboratory

def create_db_session():
    """
    Generate a SQLAlchemy session object
    """
    conn = 'mysql+mysqlconnector://ispyb:integration@192.168.33.11:3306/ispyb'
    
    engine = create_engine(conn)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def create_all():
    proposal_code = 'cm'
    proposal_number = '1001'

    session = create_db_session()

    # Try to create new test user
    person_params = {"login": "jbloggs", "given_name": "Joe", "family_name": "Bloggs"}
    person_id = person.create(session, person_params)

    # Try to create new test user (for logging in to cas)
    user = {"login": "boaty", "given_name": "Boaty", "family_name": "McBoatface"}
    user_id = person.create(session, user)

    # Create Proposal
    proposal_params = {
        "title": "Test Proposal {}{}".format(proposal_code, proposal_number),
        "proposal_code": proposal_code,
        "proposal_number": proposal_number,
        "person_id": person_id,
    }

    proposal_id = proposal.create(session, proposal_params)
    print("Proposal id = {}".format(proposal_id))

    # Create Session
    blsession_params = {
        "session_title": "Auto-generated session",
        "visit_number": "1",
        "beamline_name": "i02",
        "proposal_id": proposal_id,
    }
    bl_session_id = blsession.create(session, blsession_params)
    print("Session id = {}".format(bl_session_id))

    # Associate Session with User
    shp_params = {"person_id": person_id, "bl_session_id": bl_session_id}
    blsession.add_person(session, shp_params)

    shp_params = {"person_id": user_id, "bl_session_id": bl_session_id}
    blsession.add_person(session, shp_params)

    #
    # Shipment
    #
    # Create a labcontact first
    # Lab Contact needs to refer to a person
    labcontact_params = {
        'card_name': 'Lab contact {}'.format(''.join([proposal_code, proposal_number])),
        'person_id': person_id,
        'proposal_id': proposal_id
    }
    labcontact_id = labcontact.create(session, labcontact_params)

    # Also need a laboratory otherwise SynchWeb will not get the lab contacts 
    # because it does an inner join between the lab, contact and person
    laboratory_params = {
        'name': 'Acme Labs',
        'address': '123 Research Lane',
        'post_code': 'AB12 3CD',
        'city': 'Oxford',
        'country': 'United Kingdom',
    }
    lab_id = laboratory.create(session, laboratory_params)

    shipment_params = { 'shipping_name': 'Auto-generated shipment', 'proposal_id' : proposal_id, 'labcontact_id': labcontact_id}
    shipment_id = shipping.create(session, shipment_params)

    dewars = []
    for i in range(5):
        dewar_params = {}
        dewar_params['facility_code'] = "DLS-MX-000{}".format(i)
        dewar_params['barcode'] = "cm1001-i02-000{}".format(i)
        dewar_params['storage_location'] = "EBIC-IN-{}".format(i)
        dewar_params['dewar_status'] = "at facility"
        dewar_params['barcode'] = "cm1001-i02-000{}".format(i)
        dewar_params['shipping_id'] = shipment_id

        dewar_id = dewars.create(session, dewar_params)

        dewars.append(dewar_id)

    # Add Dewar Transport History for first couple
    for index, dewar in enumerate(dewars[0:2]):
        dewar_params = {}
        dewar_params['storage_location'] = 'EBIC-OUT-{}'.format(index)
        dewar_params['dewar_status'] = 'at-facility'
        dewar_params['dewar_id'] = dewar

        dewars.add_history(session, dewar_params)
        
    # # Add Data collection to session
    # # First create data collection group
    # dc_params = {"bl_session_id": bl_session_id}
    # dcg_id = datacollection.create_data_collection_group(session, dc_params)

    # # Next create the actual data collection
    # dc_params["data_collection_group_id"] = dcg_id
    # datacollection.create_data_collection(session, dc_params)

    # Return proposal id as we need this to delete test data
    return proposal_id



def remove_all():
    """
    Remove test proposal and all related tables 
    using cascading delete in DB
    """
    session = create_db_session()

    # Remove data collection groups and collections (no cascade here...)
    datacollection.remove_all(session)

    # Remove proposal which will remove sessions, shipments etc
    proposal.remove_all(session)


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
 
