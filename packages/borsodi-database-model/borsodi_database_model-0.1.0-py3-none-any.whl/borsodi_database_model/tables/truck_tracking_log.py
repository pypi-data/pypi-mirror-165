import enum

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String

from .base import Base


class Cameras(enum.Enum):
    one = 1
    two = 2
    three = 3


class TruckTrackingLog(Base):
    __tablename__ = 'truck_tracking_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(DateTime, nullable=False)
    camera_id = Column(Enum(Cameras), nullable=False)
    licence_plate = Column(String(15), nullable=False)
    arrived = Column(DateTime, nullable=False)
    waiting = Column(DateTime, nullable=False)
    finished = Column(DateTime, nullable=False)
    status = Column(String(10), nullable=False)
