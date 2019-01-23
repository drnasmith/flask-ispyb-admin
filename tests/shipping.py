import os
import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

def create(session, params):
    """
    Create Shipping in db

    parameters:
      session - SQLAlchemy session object
      params - Dict containing shipping info and proposal FK
    """
    shipment = models.Shipping()
    shipment.shippingName = params["shipping_name"]
    shipment.bltimeStamp = datetime.datetime.now()
    shipment.creationDate = datetime.datetime.now()

    # FK to proposal
    shipment.proposalId = params["proposal_id"]
    shipment.sendingLabContactId = params["labcontact_id"]
    shipment.returnLabContactId = params["labcontact_id"]

    session.add(shipment)
    session.commit()

    return shipment.shippingId


