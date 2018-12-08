import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models


def create_db_session():
    """
    Generate a SQLAlchemy session object
    """
    conn = "mysql+mysqlconnector://ispyb:integration@192.168.33.11:3306/ispyb"
    engine = create_engine(conn)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def create_person(session, params):
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
    except IntegrityError:
        session.rollback()
        print("Person {} already exists..".format(params["login"]))
        # Person already exists, try to get the existing one
        person = (
            session.query(models.Person)
            .filter(models.Person.login == params["login"])
            .one()
        )

    return person.personId


def create_proposal(session, params):
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

    return proposal.proposalId


def create_blsession(session, params):
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


def add_person_to_session(session, params):
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


def create_data_collection_group(session, params):
    """
    Data collections need to be associated with a group
    parameters:
      session - SQLAlchemy session object
      params - Dict containing session fk
    """
    dcg = models.DataCollectionGroup()

    dcg.sessionId = params["bl_session_id"]
    dcg.comments = "auto-generated"
    dcg.startTime = datetime.datetime.now()
    dcg.endTime = dcg.startTime + datetime.timedelta(minutes=5)
    dcg.experimentType = "experiment"

    session.add(dcg)
    session.commit()

    return dcg.dataCollectionGroupId


def create_data_collection(session, params):
    """
    Data collection 
    parameters:
      session - SQLAlchemy session object
      params - Dict containing data collection group fk
    """
    dc = models.DataCollection()

    image_dir = "/dls/i01/data/cm0000-1/"

    dc.runStatus = "Data Collection Successful"
    dc.startTime = datetime.datetime.now()
    dc.endTime = dc.startTime + datetime.timedelta(minutes=2)
    dc.axisStart = 0.0
    dc.axisEnd = 0.1
    dc.axisRange = 0.1
    dc.overlap = 0.0
    dc.startImageNumber = 1
    dc.exposureTime = 0.025
    dc.wavelength = 1.0
    dc.resolution = 1.5
    dc.detectorDistance = 100.0
    dc.xBeam = 100.0
    dc.yBeam = 100.0
    dc.comments = "auto-generated"
    dc.slitGapHorizontal = 0.05
    dc.slitGapVertical = 0.1

    dc.imageDirectory = image_dir
    dc.xtalSnapshotFullPath1 = os.path.join(image_dir, "xtalsnapshot1.png")
    dc.xtalSnapshotFullPath2 = os.path.join(image_dir, "xtalsnapshot1.png")
    dc.xtalSnapshotFullPath3 = os.path.join(image_dir, "xtalsnapshot1.png")
    dc.xtalSnapshotFullPath4 = os.path.join(image_dir, "xtalsnapshot1.png")

    # Session id here is not a FK but an integer (!?)
    dc.SESSIONID = int(params["bl_session_id"])
    dc.dataCollectionGroupId = params["data_collection_group_id"]

    session.add(dc)
    session.commit()


def get_person_id(session, params):
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


def create_all():
    session = create_db_session()

    # Try to create new test user
    person = {"login": "jbloggs", "given_name": "Joe", "family_name": "Bloggs"}
    person_id = create_person(session, person)

    # Create Proposal
    proposal = {
        "title": "Test Proposal 1",
        "proposal_code": "cm",
        "proposal_number": "1001",
        "person_id": person_id,
    }

    proposal_id = create_proposal(session, proposal)
    print("Proposal id = {}".format(proposal_id))

    # Create Session
    blsession = {
        "session_title": "Auto-generated session",
        "visit_number": "1",
        "beamline_name": "i01",
        "proposal_id": proposal_id,
    }
    bl_session_id = create_blsession(session, blsession)
    print("Session id = {}".format(bl_session_id))

    # Associate Session with User
    shp_params = {"person_id": person_id, "bl_session_id": bl_session_id}
    add_person_to_session(session, shp_params)

    # Add Data collection to session
    # First create data collection group
    dc_params = {"bl_session_id": bl_session_id}
    dcg_id = create_data_collection_group(session, dc_params)

    # Next create the actual data collection
    dc_params["data_collection_group_id"] = dcg_id
    create_data_collection(session, dc_params)

    # Return proposal id as we need this to delete test data
    return proposal_id


def remove_all_from_proposal(proposal_id):
    """
    Remove test proposal and all related tables 
    using cascading delete in DB
    """
    session = create_db_session()

    # TODO find data collections, data collection groups and remove those first
    proposal = session.query(models.Proposal).get(proposal_id)
    try:
        session.delete(proposal)
        session.commit()
    except UnmappedInstanceError:
        print("Error - proposal not found {}".format(proposal_id))
    except IntegrityError:
        print("IntegrityError - can't remove proposal {}".format(proposal_id))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--create", action="store_true", default=True, help="Create db tables")
    parser.add_argument("-r", "--remove", dest="remove", help="Try to remove proposal id provided from db")

    args = parser.parse_args()

    if args.remove:
        print("Remove DB tables for Proposal Id: {}".format(args.remove))
        remove_all_from_proposal(args.remove)
    elif args.create:
        print("Create DB tables")
        proposal_id = create_all()
        print("Created Tables for Proposal Id: {}".format(proposal_id))
 