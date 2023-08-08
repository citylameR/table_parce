from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('postgresql://user:password@localhost:5433/parser')
Session = sessionmaker(bind=engine)
session = Session()


class Auction(Base):
    __tablename__ = 'auctions'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    place = Column(String)
    region = Column(String)
    status = Column(String)
    deadline = Column(String)
    fee = Column(String)
    organizer = Column(String)


Base.metadata.create_all(engine)
