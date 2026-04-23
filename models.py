from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

"""
Timesheet Base Model (Table in db)
"""

class TimesheetEntry(Base):
    __tablename__ = "timesheet"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    type = Column(Integer, default=0)
    task = Column(String, default="TODO")
    costbearer = Column(Integer, default=0)
    duration = Column(Float, default=0.0)