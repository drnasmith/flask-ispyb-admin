from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_db_session():
    """
    Generate a SQLAlchemy session object
    """
    conn = 'mysql+mysqlconnector://ispyb:integration@192.168.33.11:3306/ispyb'
    
    engine = create_engine(conn)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session
