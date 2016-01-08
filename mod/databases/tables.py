#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, VARCHAR,ForeignKey, Float 
from sqlalchemy.orm import relationship,backref
from db import engine,Base


class User(Base):
	__tablename__ = 'users'
	id = Column(Integer,primary_key = True)
	user_phone = Column(String)
	user_name = Column(String)
	uuid = Column(String)

class Activity(Base):
	__tablename__ = 'activities'
	id = Column(Integer,primary_key = True)
	activity = Column(String)
	time = Column(String)
	leader = Column(String)
	description = Column(String)

class Partner(Base):
	__tablename__ = 'partners'
	id = Column(Integer,primary_key = True)
	activity_id = Column(String)
	user_id = Column(String)
	user_name = Column(String)
	


