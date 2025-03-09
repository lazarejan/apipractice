from sqlalchemy import  ForeignKey, create_engine, Column, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import sessionmaker, relationship
from config import settings

URL = f'postgresql://{settings.db_username}:{settings.db_pass}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

engine = create_engine(URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind = engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

Base = declarative_base()

class Posts(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, nullable=False, index=True, primary_key=True)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable= False, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, nullable=False, index=True, primary_key=True)
    email = Column(String, nullable=False, unique = True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))