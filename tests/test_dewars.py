import os
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

def create(session, params):
    """
    Create Dewar in db

    parameters:
      session - SQLAlchemy session object
      params - Dict containing dewar info and shipping FK
    """
    dewar = models.Dewar()
    dewar.storageLocation = params["storage_location"]
    dewar.dewarStatus = params["dewar_status"]
    dewar.barCode = params["barcode"]
    dewar.FACILITYCODE = params["facility_code"]
    # Default start date of now and end date +5 days
    dewar.bltimeStamp = datetime.datetime.now()

    # FK to shipping
    dewar.shippingId = params["shipping_id"]

    session.add(dewar)
    session.commit()

    return dewar.dewarId

def get_dewar(session, dewar_id):
    """
    Return dewar model based on dewar id
    """
    dewar = session.query(models.Dewar).get(dewar_id)
    return dewar

def add_history(session, params):
    """
    Function to add history for this dewar 

    parameters:
      session - SQLAlchemy session object
      params - Dict containing dewar history
    """
    dewar_history = models.DewarTransportHistory()
    dewar_history.storageLocation = params["storage_location"]
    dewar_history.arrivalDate = datetime.datetime.now()
    dewar_history.dewarStatus = params["dewar_status"]
    # FK to dewar
    dewar_history.dewarId = params["dewar_id"]

    session.add(dewar_history)
    # We also should update the dewar storage location so it matches
    dewar = get_dewar(session, dewar_history.dewarId)
    dewar.storageLocation = params['storage_location']
    session.add(dewar)

    # Commit changes
    session.commit()

    return dewar_history.DewarTransportHistoryId
