import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import event

from .database import Base, engine

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  firstname = Column(String, nullable=False)
  lastname = Column(String, nullable=False)
  email = Column(String, unique=True, nullable=False)
  password = Column(String, nullable=False)
  role_id = Column(Integer, ForeignKey("roles.id"), default=1, nullable=False)  
  is_active = Column(Boolean, default=True,)
  created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
  updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

  roles = relationship("Role", back_populates="users")
  tunes = relationship("Tune", back_populates="users")

  def __str__(self):
        return f"User(id={self.id}, firstname='{self.firstname}', lastname='{self.lastname}', email='{self.email}')"

class Role(Base):
  __tablename__ = "roles"

  id = Column(Integer, primary_key=True)
  name = Column(String)

  users = relationship("User", back_populates="roles")

class Tune(Base):
  __tablename__ = "tunes"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  code = Column(Integer,index=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
  file_name = Column(String)

  users = relationship("User", back_populates="tunes")


Base.metadata.create_all(bind=engine)


                
  