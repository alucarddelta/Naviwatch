from app import db
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


"""
Create Base flask-sqlalchemy models for inheritance by other models. All other models use vanilla SQLAlchemy so that
vanilla SQLAlchemy's superior documentation is 100% applicable to all other models.
"""


class Base(db.Model):
    """
    Abstract SQL Alchemy Model for all classes. Implements a set of standard columns and delcares an attributed that
    returns an sql table name derived from the model class name.

    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """
        default table name for sqlalchemy model

        Returns:
            string: class name

        """
        return cls.__name__

    """ Data Columns """
    xid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_modified = Column(DateTime, onupdate=datetime.datetime.utcnow)
    updated_by = Column(Integer)


class Person(Base):
    """ Thing SQL Alchemy Model """

    """ Data Columns """
    name = Column(String(255), unique=True)

    """ Relationships """
    activities = relationship('Activities')
    toilet = relationship('Toilet')


class Pet(Base):
    """ Thing SQL Alchemy Model """

    """ Data Columns """
    name = Column(String(255), unique=True)
    animal = Column(String(255), nullable=True)
    birthday = Column(String(255), nullable=True)

    """ Relationships """
    Food = relationship('Food')
    watercheck = relationship('Watercheck')
    activities = relationship('Activities')
    toilet = relationship('Toilet')


class Food(Base):
    """ Thing SQL Alchemy Model """

    """ Data Columns """
    foodtype = Column(String(255))

    """ Foreign Keys """
    pet_xid = Column(Integer, ForeignKey('Pet.xid'))
    person_xid = Column(Integer, ForeignKey('Person.xid'))

    """ Relationships """
    pet = relationship('Pet')
    person = relationship('Person')


class Watercheck(Base):
    """ Thing SQL Alchemy Model """

    """ Data Columns """
    act_type = Column(String(255))
    comment = Column(String(255), nullable=True)

    """ Foreign Keys """
    pet_xid = Column(Integer, ForeignKey('Pet.xid'))
    person_xid = Column(Integer, ForeignKey('Person.xid'))

    """ Relationships """
    pet = relationship('Pet')
    person = relationship('Person')


class Activities(Base):
    """ Thing SQL Alchemy Model """

    """ Data Columns """
    act_type = Column(String(255))
    comment = Column(String(255), nullable=True)

    """ Foreign Keys """
    pet_xid = Column(Integer, ForeignKey('Pet.xid'))
    Person_xid = Column(Integer, ForeignKey('Person.xid'))

    """ Relationships """
    pet = relationship('Pet')
    person = relationship('Person')


class Toilet(Base):
    """ Thing SQL Alchemy Model """

    """ Data Columns """
    pee = Column(Boolean)
    poo = Column(Boolean)
    accidnet = Column(Boolean)

    """ Foreign Keys """
    pet_xid = Column(Integer, ForeignKey('Pet.xid'))
    person_xid = Column(Integer, ForeignKey('Person.xid'))

    """ Relationships """
    pet = relationship('Pet')
    person = relationship('Person')


##################################################################################

class Thing(Base):
    """ Thing SQL Alchemy Model """

    """ Data Columns """
    name = Column(String(255), unique=True)
    description = Column(Text, nullable=True)

    """ Relationships """
    stuff = relationship('Stuff')


class Stuff(Base):
    """ Stuff SQL Alchemy Model """

    """ Data Columns """
    stuff = Column(String(255))

    """ Foreign Keys """
    thing_xid = Column(Integer, ForeignKey('Thing.xid'))

    """ Relationships """
    thing = relationship('Thing')
