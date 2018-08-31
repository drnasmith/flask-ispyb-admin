from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conn = 'mysql://ispyb:integration@192.168.33.11:3306/ispyb'

engine = create_engine(conn)
Session = sessionmaker(bind=engine)

session = Session()

from ispyb import models

def test_persons():
    people = session.query(models.Person).values(models.Person.login)
    for p in people:
        print p

def test_sessions():
    login='boaty'

    query = session.query(models.BLSession).join(models.SessionHasPerson).join(models.Person).join(models.Proposal)
    query = query.filter(models.Person.login==login,
                         models.Person.personId == models.SessionHasPerson.personId,
                         models.SessionHasPerson.sessionId == models.BLSession.sessionId,
                         models.BLSession.proposalId == models.Proposal.proposalId)

    records = query.values(models.BLSession.sessionId,
                           models.BLSession.proposalId,
                           models.Person.personId,
                           models.SessionHasPerson.personId.label("shp_personId"),
                           models.Proposal.title)

    for r in records:
        print r.proposalId, r.sessionId, r.personId, r.shp_personId, r.title

def test_inspections(iid=0):

    inspections = session.query(models.ContainerInspection).filter(models.ContainerInspection.containerInspectionId == iid).values(models.ContainerInspection.inspectionTypeId)

    for inspection in inspections:
        print inspection.inspectionTypeId


#test_persons()
#test_sessions()
test_inspections(1)
test_inspections(2)
test_inspections(3)

