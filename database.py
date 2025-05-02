from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import read_json

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String)
    clicks = Column(Integer, default=0)
    max_score = Column(Integer, default=0)

engine = create_engine(read_json("DATABASE_URL"))
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_or_create_user(user_id, username):
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    
    if not user:
        user = User(user_id=user_id, username=username)
        session.add(user)
        session.commit()
    
    session.close()
    return user

def update_user_score(user_id, clicks, max_score):
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    
    if user:
        user.clicks = clicks
        if max_score > user.max_score:
            user.max_score = max_score
        session.commit()
    
    session.close()
    return user