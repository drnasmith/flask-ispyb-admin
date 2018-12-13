import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from ispyb import models

data_collections = []
data_collection_groups = []

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

    data_collection_groups.append(dcg.dataCollectionGroupId)

    return dcg.dataCollectionGroupId


def create_data_collection(session, params):
    """
    Data collection 
    parameters:
      session - SQLAlchemy session object
      params - Dict containing data collection group fk
    """
    dc = models.DataCollection()

    image_dir = "/scratch/dls/i01/data/cm0000-1/"

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

    dc.dataCollectionGroupId = params["data_collection_group_id"]

    session.add(dc)
    session.commit()

    data_collections.append(dc.dataCollectionId)

    return dc.dataCollectionId

def remove_all(session):
    for id in data_collections:
        try:
            row = session.query(models.DataCollection).get(id)
            session.delete(row)
            session.commit()
        except UnmappedInstanceError:
            print("Error - data collection not found {}".format(id))
        except IntegrityError:
            print("IntegrityError - can't remove data collection {}".format(id))

    for id in data_collection_groups:
        try:
            row = session.query(models.DataCollectionGroup).get(id)
            session.delete(row)
            session.commit()
        except UnmappedInstanceError:
            print("Error - data collection group not found {}".format(id))
        except IntegrityError:
            print("IntegrityError - can't remove data collection group {}".format(id))

